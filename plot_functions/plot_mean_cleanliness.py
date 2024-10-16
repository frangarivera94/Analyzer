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

def plot_mean_cleanliness(elementos_df, aseos_df, time_aggregation='monthly', graph_type='Bar Chart', show_numbers=False, color_palette='Plotly'):
    # Convert 'FECHAHORA' to datetime
    elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
    aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')

    # Drop rows with invalid dates and create a copy
    elementos_df = elementos_df.dropna(subset=['FECHAHORA']).copy()
    aseos_df = aseos_df.dropna(subset=['FECHAHORA']).copy()

    # Create 'Period' column based on time aggregation
    if time_aggregation == 'monthly':
        elementos_df.loc[:, 'Periodo'] = elementos_df['FECHAHORA'].dt.to_period('M').astype(str)
        aseos_df.loc[:, 'Periodo'] = aseos_df['FECHAHORA'].dt.to_period('M').astype(str)
    elif time_aggregation == 'quarterly':
        elementos_df.loc[:, 'Periodo'] = elementos_df['FECHAHORA'].dt.to_period('Q').astype(str)
        aseos_df.loc[:, 'Periodo'] = aseos_df['FECHAHORA'].dt.to_period('Q').astype(str)
    else:
        elementos_df.loc[:, 'Periodo'] = elementos_df['FECHAHORA'].dt.to_period('M').astype(str)
        aseos_df.loc[:, 'Periodo'] = aseos_df['FECHAHORA'].dt.to_period('M').astype(str)

    # Group by period
    elementos_grouped = elementos_df.groupby('Periodo')['mean_cleanliness'].mean().reset_index()
    aseos_grouped = aseos_df.groupby('Periodo')['mean_cleanliness'].mean().reset_index()

    # Determine the color palette
    colors = COLOR_PALETTES.get(color_palette, px.colors.qualitative.Plotly)

    # Generate graph based on graph_type
    if graph_type == 'Bar Chart':
        fig_elementos = px.bar(
            elementos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            title='Promedio de Limpieza en el Tiempo (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )
        fig_aseos = px.bar(
            aseos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            title='Promedio de Limpieza en el Tiempo (Aseos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )

        if show_numbers:
            fig_elementos.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_aseos.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    elif graph_type == 'Line Chart':
        fig_elementos = px.line(
            elementos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            title='Promedio de Limpieza en el Tiempo (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )
        fig_aseos = px.line(
            aseos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            title='Promedio de Limpieza en el Tiempo (Aseos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )

        if show_numbers:
            fig_elementos.update_traces(texttemplate='%{text:.2f}', textposition='top center')
            fig_aseos.update_traces(texttemplate='%{text:.2f}', textposition='top center')

    else:
        return "<p>Error: Tipo de gráfico no compatible.</p>"

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

    graph_html = fig_elementos.to_html(full_html=False) + fig_aseos.to_html(full_html=False)
    return graph_html
