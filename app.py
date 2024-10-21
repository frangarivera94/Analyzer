import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pandas as pd
from werkzeug.utils import secure_filename
from data_processing import load_data
from plot_functions.plot_mean_cleanliness import plot_mean_cleanliness
from plot_functions.plot_cleaning_by_hospital_unit_and_zone import plot_cleaning_by_hospital_unit_and_zone
from plot_functions.plot_cleaning_by_zone import plot_cleaning_by_zone
from plot_functions.plot_cleaning_by_zone_and_room_type import plot_cleaning_by_zone_and_room_type
from plot_functions.plot_cleaning_by_elements_per_quarter import plot_cleaning_by_elements_per_quarter
from plot_functions.plot_cleaning_by_hospital_unit import plot_cleaning_by_hospital_unit
from datetime import datetime  # Add this import
from data_processing import get_min_max_dates
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named app.log
        logging.StreamHandler()  # Also log to console
    ]
)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        # Check if files are in the request
        if 'files[]' not in request.files:
            flash('No files part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        if not files or files[0].filename == '':
            flash('No selected files')
            return redirect(request.url)

        file_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)
            else:
                flash('Invalid file type')
                return redirect(request.url)

        # Store file paths in session
        session['file_paths'] = file_paths

        return redirect(url_for('select_graph'))

    return render_template('upload.html')

import logging

@app.route('/select_graph', methods=['GET', 'POST'])
def select_graph():
    if 'file_paths' not in session:
        return redirect(url_for('upload_files'))

    # Load the data from the uploaded files
    elementos_df, aseos_df = load_data(session['file_paths'])

    # Get min and max date
    min_date, max_date = get_min_max_dates(elementos_df, aseos_df)

    # Log the dates before rendering the template
    logging.info(f"Passing min_date to template: {min_date}")
    logging.info(f"Passing max_date to template: {max_date}")

    templates = {
        'Mean Cleanliness Over Time': 'mean_cleanliness',
        'Cleaning by Hospital Unit and Zone': 'plot_cleaning_by_hospital_unit_and_zone',
        'Cleaning by Zone': 'cleaning_by_zone',
        'Cleaning by Zone and Room Type': 'cleaning_by_zone_and_room_type',
        'Cleaning by Elements per Quarter': 'cleaning_by_elements_per_quarter',
        'Custom Graph': 'custom'
    }

    if request.method == 'POST':
        template = request.form['template']
        print(f"Template selected: {template}")  # Debug: Template selected by the user
        time_aggregation = request.form.get('time_aggregation', 'monthly')
        graph_type = request.form.get('graph_type', 'Line Chart')
        show_numbers = 'show_numbers' in request.form
        color_palette = request.form.get('color_palette', 'Plotly')

        # Verify if the selected template is mapped to the correct graph function
        print(f"Template being mapped to graph function: {template}")

        if template != 'custom':
            graph_html = generate_template_graph(template, elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette)
            return render_template('display_graph.html', graph_html=graph_html, show_numbers=show_numbers, color_palette=color_palette, min_date=min_date, max_date=max_date)
        else:
            flash('Custom graph generation is not implemented yet.')
            return redirect(url_for('select_graph'))




    return render_template('select_graph.html', templates=templates.keys(), min_date=min_date, max_date=max_date)


def generate_template_graph(template_name, elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette):
    # Ensure all template names match exactly
    if template_name == 'mean_cleanliness':
        graph_html = plot_mean_cleanliness(elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette)
    elif template_name == 'cleaning_by_zone':
        graph_html = plot_cleaning_by_zone(elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette)
    elif template_name == 'cleaning_by_zone_and_room_type':
        graph_html = plot_cleaning_by_zone_and_room_type(elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette)
    elif template_name == 'cleaning_by_elements_per_quarter':
        graph_html = plot_cleaning_by_elements_per_quarter(elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette)
    elif template_name == 'cleaning_by_hospital_unit':
        graph_html = plot_cleaning_by_hospital_unit(elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette)
    elif template_name == 'cleaning_by_hospital_unit_and_zone':
        # Make sure the function name and template name match exactly
        graph_html = plot_cleaning_by_hospital_unit_and_zone(elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette)
    else:
        print(f"Error: No graph function found for template {template_name}")  # Debugging message
        return "<p>Error: No matching graph function found for the selected template.</p>"

    return graph_html




@app.route('/update_graph', methods=['POST'])
def update_graph():
    # Get the data from the POST request
    data = request.get_json()
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    graph_type = data.get('graph_type', 'Line Chart')

    # Convert the date strings to datetime objects
    start_date = pd.to_datetime(start_date_str, errors='coerce')
    end_date = pd.to_datetime(end_date_str, errors='coerce')

    # Load the filtered data from session
    if 'file_paths' in session:
        elementos_df, aseos_df = load_data(session['file_paths'])

        # Filter the data based on the selected date range
        if 'FECHAHORA' in elementos_df.columns:
            elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
            elementos_df = elementos_df[
                (elementos_df['FECHAHORA'] >= start_date) & (elementos_df['FECHAHORA'] <= end_date)]
        if 'FECHAHORA' in aseos_df.columns:
            aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')
            aseos_df = aseos_df[(aseos_df['FECHAHORA'] >= start_date) & (aseos_df['FECHAHORA'] <= end_date)]

        # Generate the updated graph
        graph_html = generate_template_graph('mean_cleanliness', elementos_df, aseos_df, 'monthly', graph_type,
                                             show_numbers=True, color_palette='Plotly')

        return jsonify({"graph_html": graph_html})

    return jsonify({"error": "Data not found"}), 400

@app.route('/toggle_numbers', methods=['POST'])
def toggle_numbers():
    elementos_df, aseos_df = load_data(session['file_paths'])
    template = request.form['template']
    time_aggregation = request.form.get('time_aggregation', 'monthly')
    graph_type = request.form.get('graph_type', 'Line Chart')
    show_numbers = request.form.get('show_numbers') == 'True'
    color_palette = request.form.get('color_palette', 'Plotly')

    graph_html = generate_template_graph(template, elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette)
    return render_template('display_graph.html', graph_html=graph_html, show_numbers=show_numbers, color_palette=color_palette)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
