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

def plot_cleaning_by_hospital(elementos_df, aseos_df, time_aggregation='monthly', graph_type='Bar Chart', show_numbers=False, color_palette='Plotly'):
    # Convert 'FECHAHORA' to datetime
    elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
    aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')

    # Ensure 'CENTRO HOSP.' column exists before proceeding
    if 'CENTRO HOSP.' not in elementos_df.columns or 'CENTRO HOSP.' not in aseos_df.columns:
        return "<p>Error: Columna 'CENTRO HOSP.' no encontrada en los datos.</p>"

    # Drop rows with invalid dates and missing 'CENTRO HOSP.'
    elementos_df = elementos_df.dropna(subset=['FECHAHORA', 'CENTRO HOSP.']).copy()
    aseos_df = aseos_df.dropna(subset=['FECHAHORA', 'CENTRO HOSP.']).copy()

    # Ensure 'CENTRO HOSP.' is of type string
    elementos_df['CENTRO HOSP.'] = elementos_df['CENTRO HOSP.'].astype(str)
    aseos_df['CENTRO HOSP.'] = aseos_df['CENTRO HOSP.'].astype(str)

    # Create 'Periodo' column based on time aggregation
    if time_aggregation == 'monthly':
        elementos_df['Periodo'] = elementos_df['FECHAHORA'].dt.to_period('M').astype(str)
        aseos_df['Periodo'] = aseos_df['FECHAHORA'].dt.to_period('M').astype(str)
    elif time_aggregation == 'quarterly':
        elementos_df['Periodo'] = elementos_df['FECHAHORA'].dt.to_period('Q').astype(str)
        aseos_df['Periodo'] = aseos_df['FECHAHORA'].dt.to_period('Q').astype(str)
    else:
        elementos_df['Periodo'] = elementos_df['FECHAHORA'].dt.to_period('M').astype(str)
        aseos_df['Periodo'] = aseos_df['FECHAHORA'].dt.to_period('M').astype(str)

    # Group by period and hospital
    elementos_grouped = elementos_df.groupby(['Periodo', 'CENTRO HOSP.'])['mean_cleanliness'].mean().reset_index()
    aseos_grouped = aseos_df.groupby(['Periodo', 'CENTRO HOSP.'])['mean_cleanliness'].mean().reset_index()

    # Determine the color palette
    colors = COLOR_PALETTES.get(color_palette, px.colors.qualitative.Plotly)

    # Generate graph based on graph_type
    if graph_type == 'Bar Chart':
        fig_elementos = px.bar(
            elementos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            color='CENTRO HOSP.',
            barmode='group',
            title='Promedio de Limpieza por Hospital (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )
        fig_aseos = px.bar(
            aseos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            color='CENTRO HOSP.',
            barmode='group',
            title='Promedio de Limpieza por Hospital (Aseos)',
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
            x='Periodo',
            y='mean_cleanliness',
            color='CENTRO HOSP.',
            title='Promedio de Limpieza por Hospital (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )
        fig_aseos = px.line(
            aseos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            color='CENTRO HOSP.',
            title='Promedio de Limpieza por Hospital (Aseos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )

        # Show numbers on graph if selected (for line chart)
        if show_numbers:
            fig_elementos.update_traces(texttemplate='%{text:.2f}', textposition='top center')
            fig_aseos.update_traces(texttemplate='%{text:.2f}', textposition='top center')

    else:
        return "<p>Error: Tipo de gráfico no compatible.</p>"

    # Update x-axis layout for cleaner period display
    fig_elementos.update_layout(
        xaxis_title='Periodo',
        yaxis_title='Promedio de Limpieza',
        xaxis={'type': 'category'},
    )
    fig_aseos.update_layout(
        xaxis_title='Periodo',
        yaxis_title='Promedio de Limpieza',
        xaxis={'type': 'category'},
    )

    # Combine the two figures into one HTML
    graph_html = fig_elementos.to_html(full_html=False) + fig_aseos.to_html(full_html=False)
    return graph_html
