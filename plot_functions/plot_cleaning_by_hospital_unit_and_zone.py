# import pandas as pd
# import plotly.express as px
#
# # Predefined color palettes
# COLOR_PALETTES = {
#     'Plotly': px.colors.qualitative.Plotly,
#     'Viridis': px.colors.sequential.Viridis,
#     'Cividis': px.colors.sequential.Cividis,
#     'Pastel': px.colors.qualitative.Pastel,
#     'Dark': px.colors.qualitative.Dark2,
#     'Bold': px.colors.qualitative.Bold
# }
#
# def plot_cleaning_by_hospital_unit_and_zone(elementos_df, aseos_df, time_aggregation='monthly', graph_type='Bar Chart', show_numbers=False, color_palette='Plotly'):
#     # Convert 'FECHAHORA' to datetime
#     elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
#     aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')
#
#     # Ensure 'UNIDAD HOSP.' and 'ZONA' columns exist before proceeding
#     if 'UNIDAD HOSP.' not in elementos_df.columns or 'ZONA' not in elementos_df.columns or \
#        'UNIDAD HOSP.' not in aseos_df.columns or 'ZONA' not in aseos_df.columns:
#         return "<p>Error: Columnas 'UNIDAD HOSP.' o 'ZONA' no encontradas en los datos.</p>"
#
#     # Drop rows with invalid dates and missing 'UNIDAD HOSP.' or 'ZONA'
#     elementos_df = elementos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.', 'ZONA']).copy()
#     aseos_df = aseos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.', 'ZONA']).copy()
#
#     # Ensure 'UNIDAD HOSP.' and 'ZONA' are of type string
#     elementos_df['UNIDAD HOSP.'] = elementos_df['UNIDAD HOSP.'].astype(str)
#     elementos_df['ZONA'] = elementos_df['ZONA'].astype(str)
#     aseos_df['UNIDAD HOSP.'] = aseos_df['UNIDAD HOSP.'].astype(str)
#     aseos_df['ZONA'] = aseos_df['ZONA'].astype(str)
#
#     # Create 'Periodo' column based on time aggregation
#     if time_aggregation == 'monthly':
#         elementos_df['Periodo'] = elementos_df['FECHAHORA'].dt.to_period('M').astype(str)
#         aseos_df['Periodo'] = aseos_df['FECHAHORA'].dt.to_period('M').astype(str)
#     elif time_aggregation == 'quarterly':
#         elementos_df['Periodo'] = elementos_df['FECHAHORA'].dt.to_period('Q').astype(str)
#         aseos_df['Periodo'] = aseos_df['FECHAHORA'].dt.to_period('Q').astype(str)
#     else:
#         elementos_df['Periodo'] = elementos_df['FECHAHORA'].dt.to_period('M').astype(str)
#         aseos_df['Periodo'] = aseos_df['FECHAHORA'].dt.to_period('M').astype(str)
#
#     # Group by period, hospital unit, and zone
#     elementos_grouped = elementos_df.groupby(['Periodo', 'UNIDAD HOSP.', 'ZONA'])['mean_cleanliness'].mean().reset_index()
#     aseos_grouped = aseos_df.groupby(['Periodo', 'UNIDAD HOSP.', 'ZONA'])['mean_cleanliness'].mean().reset_index()
#
#     # Determine the color palette
#     colors = COLOR_PALETTES.get(color_palette, px.colors.qualitative.Plotly)
#
#     # Generate graph based on graph_type
#     if graph_type == 'Bar Chart':
#         fig_elementos = px.bar(
#             elementos_grouped,
#             x='Periodo',
#             y='mean_cleanliness',
#             color='ZONA',
#             facet_col='UNIDAD HOSP.',
#             barmode='group',
#             title='Promedio de Limpieza por Unidad Hospitalaria y Zona (Elementos)',
#             text='mean_cleanliness' if show_numbers else None,
#             color_discrete_sequence=colors
#         )
#         fig_aseos = px.bar(
#             aseos_grouped,
#             x='Periodo',
#             y='mean_cleanliness',
#             color='ZONA',
#             facet_col='UNIDAD HOSP.',
#             barmode='group',
#             title='Promedio de Limpieza por Unidad Hospitalaria y Zona (Aseos)',
#             text='mean_cleanliness' if show_numbers else None,
#             color_discrete_sequence=colors
#         )
#
#         # Show numbers on graph if selected
#         if show_numbers:
#             fig_elementos.update_traces(texttemplate='%{text:.2f}', textposition='outside')
#             fig_aseos.update_traces(texttemplate='%{text:.2f}', textposition='outside')
#
#     elif graph_type == 'Line Chart':
#         fig_elementos = px.line(
#             elementos_grouped,
#             x='Periodo',
#             y='mean_cleanliness',
#             color='ZONA',
#             facet_col='UNIDAD HOSP.',
#             title='Promedio de Limpieza por Unidad Hospitalaria y Zona (Elementos)',
#             text='mean_cleanliness' if show_numbers else None,
#             color_discrete_sequence=colors
#         )
#         fig_aseos = px.line(
#             aseos_grouped,
#             x='Periodo',
#             y='mean_cleanliness',
#             color='ZONA',
#             facet_col='UNIDAD HOSP.',
#             title='Promedio de Limpieza por Unidad Hospitalaria y Zona (Aseos)',
#             text='mean_cleanliness' if show_numbers else None,
#             color_discrete_sequence=colors
#         )
#
#         # Show numbers on graph if selected (for line chart)
#         if show_numbers:
#             fig_elementos.update_traces(texttemplate='%{text:.2f}', textposition='top center')
#             fig_aseos.update_traces(texttemplate='%{text:.2f}', textposition='top center')
#
#     else:
#         return "<p>Error: Tipo de gráfico no compatible.</p>"
#
#     # Update x-axis layout for cleaner period display
#     fig_elementos.update_layout(
#         xaxis_title='Periodo',
#         yaxis_title='Promedio de Limpieza',
#         xaxis={'type': 'category'},
#     )
#     fig_aseos.update_layout(
#         xaxis_title='Periodo',
#         yaxis_title='Promedio de Limpieza',
#         xaxis={'type': 'category'},
#     )
#
#     # Combine the two figures into one HTML
#     graph_html = fig_elementos.to_html(full_html=False) + fig_aseos.to_html(full_html=False)
#     return graph_html


import pandas as pd
import plotly.express as px

def plot_cleaning_by_hospital_unit_and_zone(elementos_df, aseos_df, time_aggregation, graph_type, show_numbers, color_palette):
    # Convert FECHAHORA to datetime format
    elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
    aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')

    # Drop rows with invalid dates
    elementos_df = elementos_df.dropna(subset=['FECHAHORA'])
    aseos_df = aseos_df.dropna(subset=['FECHAHORA'])

    # Combine the dataframes
    combined_df = pd.concat([elementos_df, aseos_df], ignore_index=True)
    combined_df['FECHAHORA'] = pd.to_datetime(combined_df['FECHAHORA'], errors='coerce')

    # Ensure that the cleanliness column is numeric
    combined_df['mean_cleanliness'] = pd.to_numeric(combined_df['mean_cleanliness'], errors='coerce')

    # Drop rows with invalid cleanliness values
    combined_df = combined_df.dropna(subset=['mean_cleanliness'])

    # Add a Period column based on the selected time aggregation
    if time_aggregation == 'monthly':
        combined_df['Period'] = combined_df['FECHAHORA'].dt.to_period('M').astype(str)
    elif time_aggregation == 'quarterly':
        combined_df['Period'] = combined_df['FECHAHORA'].dt.to_period('Q').astype(str)
    else:
        combined_df['Period'] = combined_df['FECHAHORA'].dt.to_period('M').astype(str)

    # Group by hospital unit, zone, and period to calculate the mean cleanliness
    grouped_df = combined_df.groupby(['UNIDAD HOSP.', 'ZONA', 'Period'])['mean_cleanliness'].mean().reset_index()

    # Sort by hospital unit to ensure proper plotting order
    grouped_df = grouped_df.sort_values(by=['UNIDAD HOSP.', 'ZONA', 'Period'])

    # Initialize an empty list to collect HTML of all graphs
    all_graphs_html = []

    # Loop through each unique hospital unit
    for hospital_unit in grouped_df['UNIDAD HOSP.'].unique():
        unit_df = grouped_df[grouped_df['UNIDAD HOSP.'] == hospital_unit]

        # Generate graph based on graph_type
        if graph_type == 'Bar Chart':
            fig = px.bar(
                unit_df,
                x='Period',
                y='mean_cleanliness',
                color='ZONA',
                barmode='group',
                title=f'Promedio de Limpieza en {hospital_unit} por Zona',
                text='mean_cleanliness' if show_numbers else None,
                color_discrete_sequence=px.colors.qualitative.__dict__.get(color_palette, px.colors.qualitative.Plotly)
            )

            # Show numbers on graph if selected
            if show_numbers:
                fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

        elif graph_type == 'Line Chart':
            fig = px.line(
                unit_df,
                x='Period',
                y='mean_cleanliness',
                color='ZONA',
                title=f'Promedio de Limpieza en {hospital_unit} por Zona',
                text='mean_cleanliness' if show_numbers else None,
                color_discrete_sequence=px.colors.qualitative.__dict__.get(color_palette, px.colors.qualitative.Plotly)
            )

            # Show numbers on graph if selected (for line chart)
            if show_numbers:
                fig.update_traces(texttemplate='%{text:.2f}', textposition='top center', mode='lines+markers+text')

        else:
            return "<p>Error: Tipo de gráfico no compatible.</p>"

        # Update x-axis layout for cleaner period display
        fig.update_layout(
            xaxis_title='Periodo',
            yaxis_title='Promedio de Limpieza',
            xaxis={'type': 'category'},
        )

        # Append the graph's HTML representation to the list
        all_graphs_html.append(fig.to_html(full_html=False))

    # Combine all graphs into one HTML output
    combined_html = "".join(all_graphs_html)

    return combined_html
