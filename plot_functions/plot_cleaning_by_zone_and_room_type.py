import pandas as pd
import plotly.express as px

# Predefined color palettes
COLOR_PALETTES = {
    'Plotly': px.colors.qualitative.Plotly,
    'Viridis': px.colors.sequential.Viridis,
    'Cividis': px.colors.sequential.Cividis,
    'Pastel': px.colors.qualitative.Pastel,
    'Dark': px.colors.qualitative.Dark2,
    'Bold': px.colors.qualitative.Bold
}

def plot_cleaning_by_zone_and_room_type(elementos_df, aseos_df, time_aggregation=None, graph_type='Bar Chart', show_numbers=False, color_palette='Plotly'):
    # Ensure necessary columns exist
    required_columns = ['ZONA', 'TIPO SALA']
    for col in required_columns:
        if col not in elementos_df.columns or col not in aseos_df.columns:
            return f"<p>Error: Column '{col}' not found in data.</p>"

    elementos_df['ZONA'] = elementos_df['ZONA'].astype(str)
    elementos_df['TIPO SALA'] = elementos_df['TIPO SALA'].astype(str)
    aseos_df['ZONA'] = aseos_df['ZONA'].astype(str)
    aseos_df['TIPO SALA'] = aseos_df['TIPO SALA'].astype(str)

    # Calculate mean cleanliness by zone and room type
    elementos_grouped = elementos_df.groupby(['ZONA', 'TIPO SALA'])['mean_cleanliness'].mean().reset_index()
    aseos_grouped = aseos_df.groupby(['ZONA', 'TIPO SALA'])['mean_cleanliness'].mean().reset_index()

    # Determine the color palette
    colors = COLOR_PALETTES.get(color_palette, px.colors.qualitative.Plotly)

    # Generate the appropriate graph type based on user input
    if graph_type == 'Bar Chart':
        fig_elementos = px.bar(
            elementos_grouped,
            x='ZONA',
            y='mean_cleanliness',
            color='TIPO SALA',
            barmode='group',
            title='Mean Cleanliness by Zone and Room Type (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )

        fig_aseos = px.bar(
            aseos_grouped,
            x='ZONA',
            y='mean_cleanliness',
            color='TIPO SALA',
            barmode='group',
            title='Mean Cleanliness by Zone and Room Type (Aseos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )

        # Show numbers on graph if selected
        if show_numbers:
            fig_elementos.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_aseos.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    elif graph_type == 'Line Chart':
        fig_elementos = px.line(
            elementos_grouped,
            x='ZONA',
            y='mean_cleanliness',
            color='TIPO SALA',
            title='Mean Cleanliness by Zone and Room Type (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )

        fig_aseos = px.line(
            aseos_grouped,
            x='ZONA',
            y='mean_cleanliness',
            color='TIPO SALA',
            title='Mean Cleanliness by Zone and Room Type (Aseos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )

        # Show numbers on graph if selected (for line chart)
        if show_numbers:
            fig_elementos.update_traces(texttemplate='%{text:.2f}', textposition='top center')
            fig_aseos.update_traces(texttemplate='%{text:.2f}', textposition='top center')

    else:
        return "<p>Error: Unsupported graph type.</p>"

    # Update x-axis layout for cleaner zone display
    fig_elementos.update_layout(
        xaxis_title='Zone',
        yaxis_title='Mean Cleanliness',
        xaxis={'type': 'category'},
    )
    fig_aseos.update_layout(
        xaxis_title='Zone',
        yaxis_title='Mean Cleanliness',
        xaxis={'type': 'category'},
    )

    # Combine the two figures into one HTML
    graph_html = fig_elementos.to_html(full_html=False) + fig_aseos.to_html(full_html=False)
    return graph_html
