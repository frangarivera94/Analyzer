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

def plot_cleaning_by_hospital_unit(elementos_df, aseos_df, time_aggregation='monthly', graph_type='Bar Chart', show_numbers=False, color_palette='Plotly'):
    # Ensure 'UNIDAD HOSP.' column exists
    if 'UNIDAD HOSP.' not in elementos_df.columns or 'UNIDAD HOSP.' not in aseos_df.columns:
        return "<p>Error: 'UNIDAD HOSP.' column not found in data.</p>"

    # Convert 'FECHAHORA' to datetime
    elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
    aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')

    # Drop rows with invalid dates and missing 'UNIDAD HOSP.' and make a copy to avoid SettingWithCopyWarning
    elementos_df = elementos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.']).copy()
    aseos_df = aseos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.']).copy()

    # Ensure 'UNIDAD HOSP.' is of type string
    elementos_df['UNIDAD HOSP.'] = elementos_df.loc[:, 'UNIDAD HOSP.'].astype(str)
    aseos_df['UNIDAD HOSP.'] = aseos_df.loc[:, 'UNIDAD HOSP.'].astype(str)

    # Create 'Period' column based on time aggregation
    if time_aggregation == 'monthly':
        elementos_df['Period'] = elementos_df['FECHAHORA'].dt.to_period('M').astype(str)
        aseos_df['Period'] = aseos_df['FECHAHORA'].dt.to_period('M').astype(str)
    elif time_aggregation == 'quarterly':
        elementos_df['Period'] = elementos_df['FECHAHORA'].dt.to_period('Q').astype(str)
        aseos_df['Period'] = aseos_df['FECHAHORA'].dt.to_period('Q').astype(str)
    else:
        elementos_df['Period'] = elementos_df['FECHAHORA'].dt.to_period('M').astype(str)
        aseos_df['Period'] = aseos_df['FECHAHORA'].dt.to_period('M').astype(str)

    # Group by period and hospital unit
    elementos_grouped = elementos_df.groupby(['Period', 'UNIDAD HOSP.'])['mean_cleanliness'].mean().reset_index()
    aseos_grouped = aseos_df.groupby(['Period', 'UNIDAD HOSP.'])['mean_cleanliness'].mean().reset_index()

    # Determine the color palette
    colors = COLOR_PALETTES.get(color_palette, px.colors.qualitative.Plotly)

    # Generate graph based on graph_type
    if graph_type == 'Bar Chart':
        fig_elementos = px.bar(
            elementos_grouped,
            x='Period',
            y='mean_cleanliness',
            color='UNIDAD HOSP.',
            barmode='group',
            title='Mean Cleanliness per Hospital Unit (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )
        fig_aseos = px.bar(
            aseos_grouped,
            x='Period',
            y='mean_cleanliness',
            color='UNIDAD HOSP.',
            barmode='group',
            title='Mean Cleanliness per Hospital Unit (Aseos)',
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
            x='Period',
            y='mean_cleanliness',
            color='UNIDAD HOSP.',
            title='Mean Cleanliness per Hospital Unit (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )
        fig_aseos = px.line(
            aseos_grouped,
            x='Period',
            y='mean_cleanliness',
            color='UNIDAD HOSP.',
            title='Mean Cleanliness per Hospital Unit (Aseos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )

        # Show numbers on graph if selected (for line chart)
        if show_numbers:
            fig_elementos.update_traces(texttemplate='%{text:.2f}', textposition='top center')
            fig_aseos.update_traces(texttemplate='%{text:.2f}', textposition='top center')

    else:
        return "<p>Error: Unsupported graph type.</p>"

    # Update x-axis layout for cleaner period display
    fig_elementos.update_layout(
        xaxis_title='Period',
        yaxis_title='Mean Cleanliness',
        xaxis={'type': 'category'},
    )
    fig_aseos.update_layout(
        xaxis_title='Period',
        yaxis_title='Mean Cleanliness',
        xaxis={'type': 'category'},
    )

    # Combine the two figures into one HTML
    graph_html = fig_elementos.to_html(full_html=False) + fig_aseos.to_html(full_html=False)
    return graph_html
