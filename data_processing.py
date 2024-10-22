# data_processing.py

import pandas as pd
import plotly.express as px

def load_data(file_paths):
    elementos_data = []
    aseos_data = []

    for file_path in file_paths:
        if 'elementos' in file_path.lower():
            df = pd.read_excel(file_path)
            elementos_data.append(df)
        elif 'aseos' in file_path.lower():
            df = pd.read_excel(file_path)
            aseos_data.append(df)

    elementos_df = pd.concat(elementos_data, ignore_index=True)
    aseos_df = pd.concat(aseos_data, ignore_index=True)

    # Select only the numeric columns for mean cleanliness calculation
    elementos_numeric_columns = elementos_df.select_dtypes(include='number').columns
    aseos_numeric_columns = aseos_df.select_dtypes(include='number').columns

    # Replace negative values with NaN using DataFrame.apply
    elementos_df[elementos_numeric_columns] = elementos_df[elementos_numeric_columns].apply(
        lambda col: col.where(col >= 0)
    )
    aseos_df[aseos_numeric_columns] = aseos_df[aseos_numeric_columns].apply(
        lambda col: col.where(col >= 0)
    )

    # Create the mean cleanliness column for both DataFrames
    elementos_df['mean_cleanliness'] = elementos_df[elementos_numeric_columns].mean(axis=1, skipna=True)
    aseos_df['mean_cleanliness'] = aseos_df[aseos_numeric_columns].mean(axis=1, skipna=True)

    return elementos_df, aseos_df


import logging

def get_min_max_dates(elementos_df, aseos_df):
    # Convert 'FECHAHORA' columns to datetime, coercing errors to NaT
    elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
    aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')

    # Drop rows with NaT in 'FECHAHORA'
    elementos_df = elementos_df.dropna(subset=['FECHAHORA'])
    aseos_df = aseos_df.dropna(subset=['FECHAHORA'])

    # Get the min and max dates across both dataframes
    min_date = min(elementos_df['FECHAHORA'].min(), aseos_df['FECHAHORA'].min())
    max_date = max(elementos_df['FECHAHORA'].max(), aseos_df['FECHAHORA'].max())

    # Log the min and max dates before returning
    logging.info(f"Calculated min_date: {min_date}")
    logging.info(f"Calculated max_date: {max_date}")

    return min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')


def generate_overview_charts(elementos_df, aseos_df):
    # Combine both dataframes
    combined_df = pd.concat([elementos_df, aseos_df], ignore_index=True)

    # Drop invalid FECHAHORA entries
    combined_df['FECHAHORA'] = pd.to_datetime(combined_df['FECHAHORA'], errors='coerce')
    combined_df = combined_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.']).copy()

    # Ensure 'UNIDAD HOSP.' is of type string
    combined_df['UNIDAD HOSP.'] = combined_df['UNIDAD HOSP.'].astype(str)

    # Group by 'UNIDAD HOSP.' to get the count of data points for each unit
    unidad_counts = combined_df['UNIDAD HOSP.'].value_counts().reset_index()
    unidad_counts.columns = ['UNIDAD HOSP.', 'Count']

    # Generate Bar Chart
    bar_fig = px.bar(
        unidad_counts,
        x='UNIDAD HOSP.',
        y='Count',
        title='Número de Puntos de Datos por Unidad Hospitalaria',
        color='UNIDAD HOSP.',
        text='Count',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    bar_fig.update_traces(texttemplate='%{text}', textposition='outside')
    bar_fig.update_layout(height=1000)

    # Generate Pie Chart
    pie_fig = px.pie(
        unidad_counts,
        names='UNIDAD HOSP.',
        values='Count',
        title='Proporción de Puntos de Datos por Unidad Hospitalaria',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    # Combine both charts into HTML
    overview_html = bar_fig.to_html(full_html=False) + pie_fig.to_html(full_html=False)

    return overview_html
