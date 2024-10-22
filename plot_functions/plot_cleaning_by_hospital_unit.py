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
# def plot_cleaning_by_hospital_unit(elementos_df, aseos_df, time_aggregation='monthly', graph_type='Bar Chart', show_numbers=False, color_palette='Plotly'):
#     # Ensure 'UNIDAD HOSP.' column exists
#     if 'UNIDAD HOSP.' not in elementos_df.columns or 'UNIDAD HOSP.' not in aseos_df.columns:
#         return "<p>Error: Columna 'UNIDAD HOSP.' no encontrada en los datos.</p>"
#
#     # Convert 'FECHAHORA' to datetime
#     elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
#     aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')
#
#     # Drop rows with invalid dates and missing 'UNIDAD HOSP.' and make a copy to avoid SettingWithCopyWarning
#     elementos_df = elementos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.']).copy()
#     aseos_df = aseos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.']).copy()
#
#     # Ensure 'UNIDAD HOSP.' is of type string
#     elementos_df['UNIDAD HOSP.'] = elementos_df.loc[:, 'UNIDAD HOSP.'].astype(str)
#     aseos_df['UNIDAD HOSP.'] = aseos_df.loc[:, 'UNIDAD HOSP.'].astype(str)
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
#     # Group by period and hospital unit
#     elementos_grouped = elementos_df.groupby(['Periodo', 'UNIDAD HOSP.'])['mean_cleanliness'].mean().reset_index()
#     aseos_grouped = aseos_df.groupby(['Periodo', 'UNIDAD HOSP.'])['mean_cleanliness'].mean().reset_index()
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
#             color='UNIDAD HOSP.',
#             barmode='group',
#             title='Promedio de Limpieza por Unidad Hospitalaria (Elementos)',
#             text='mean_cleanliness' if show_numbers else None,
#             color_discrete_sequence=colors
#         )
#         fig_aseos = px.bar(
#             aseos_grouped,
#             x='Periodo',
#             y='mean_cleanliness',
#             color='UNIDAD HOSP.',
#             barmode='group',
#             title='Promedio de Limpieza por Unidad Hospitalaria (Aseos)',
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
#             color='UNIDAD HOSP.',
#             title='Promedio de Limpieza por Unidad Hospitalaria (Elementos)',
#             text='mean_cleanliness' if show_numbers else None,
#             color_discrete_sequence=colors
#         )
#         fig_aseos = px.line(
#             aseos_grouped,
#             x='Periodo',
#             y='mean_cleanliness',
#             color='UNIDAD HOSP.',
#             title='Promedio de Limpieza por Unidad Hospitalaria (Aseos)',
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


#------------------------------------------------------------------------------------------


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
# def plot_cleaning_by_hospital_unit(elementos_df, aseos_df, time_aggregation='monthly', graph_type='Bar Chart', show_numbers=False, color_palette='Plotly'):
#     # Convert 'FECHAHORA' to datetime
#     print("Converting 'FECHAHORA' to datetime...")  # Debug statement
#     elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
#     aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')
#
#     # Drop rows with invalid dates and missing 'UNIDAD HOSP.' and make a copy to avoid SettingWithCopyWarning
#     elementos_df = elementos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.']).copy()
#     aseos_df = aseos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.']).copy()
#
#     # Ensure 'UNIDAD HOSP.' is of type string
#     elementos_df['UNIDAD HOSP.'] = elementos_df['UNIDAD HOSP.'].astype(str)
#     aseos_df['UNIDAD HOSP.'] = aseos_df['UNIDAD HOSP.'].astype(str)
#
#     # Create 'Periodo' column based on time aggregation
#     print("Creating 'Periodo' column based on time aggregation...")  # Debug statement
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
#     # Debug statement to check if 'Periodo' column is created properly
#     print(f"Columns in elementos_df: {elementos_df.columns}")
#     print(f"Columns in aseos_df: {aseos_df.columns}")
#
#     # Check if 'Periodo' column exists before proceeding
#     if 'Periodo' not in elementos_df.columns or 'Periodo' not in aseos_df.columns:
#         return "<p>Error: Columna 'Periodo' no encontrada. Asegúrese de que 'FECHAHORA' se haya convertido correctamente.</p>"
#
#     # Group by period and hospital unit
#     elementos_grouped = elementos_df.groupby(['Periodo', 'UNIDAD HOSP.'])['mean_cleanliness'].mean().reset_index()
#     aseos_grouped = aseos_df.groupby(['Periodo', 'UNIDAD HOSP.'])['mean_cleanliness'].mean().reset_index()
#
#     # Determine the color palette
#     colors = COLOR_PALETTES.get(color_palette, px.colors.qualitative.Plotly)
#
#     # Generate general graphs for all hospital units
#     if graph_type == 'Bar Chart':
#         fig_elementos = px.bar(
#             elementos_grouped,
#             x='Periodo',
#             y='mean_cleanliness',
#             color='UNIDAD HOSP.',
#             barmode='group',
#             title='Promedio de Limpieza por Unidad Hospitalaria (Elementos)',
#             text='mean_cleanliness' if show_numbers else None,
#             color_discrete_sequence=colors
#         )
#         fig_aseos = px.bar(
#             aseos_grouped,
#             x='Periodo',
#             y='mean_cleanliness',
#             color='UNIDAD HOSP.',
#             barmode='group',
#             title='Promedio de Limpieza por Unidad Hospitalaria (Aseos)',
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
#             color='UNIDAD HOSP.',
#             title='Promedio de Limpieza por Unidad Hospitalaria (Elementos)',
#             text='mean_cleanliness' if show_numbers else None,
#             color_discrete_sequence=colors
#         )
#         fig_aseos = px.line(
#             aseos_grouped,
#             x='Periodo',
#             y='mean_cleanliness',
#             color='UNIDAD HOSP.',
#             title='Promedio de Limpieza por Unidad Hospitalaria (Aseos)',
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
#     # Combine the two general figures into one HTML
#     all_graphs_html = fig_elementos.to_html(full_html=False) + fig_aseos.to_html(full_html=False)
#
#     # Now generate individual graphs for each hospital unit and its room types (TIPO SALA)
#     for unidad in elementos_df['UNIDAD HOSP.'].unique():
#         unit_df = elementos_df[elementos_df['UNIDAD HOSP.'] == unidad]
#         unit_grouped = unit_df.groupby(['Periodo', 'TIPO SALA'])['mean_cleanliness'].mean().reset_index()
#
#         if graph_type == 'Bar Chart':
#             fig_unit = px.bar(
#                 unit_grouped,
#                 x='Periodo',
#                 y='mean_cleanliness',
#                 color='TIPO SALA',
#                 barmode='group',
#                 title=f'Promedio de Limpieza en {unidad} por Tipo de Sala',
#                 text='mean_cleanliness' if show_numbers else None,
#                 color_discrete_sequence=colors
#             )
#             if show_numbers:
#                 fig_unit.update_traces(texttemplate='%{text:.2f}', textposition='outside')
#
#         elif graph_type == 'Line Chart':
#             fig_unit = px.line(
#                 unit_grouped,
#                 x='Periodo',
#                 y='mean_cleanliness',
#                 color='TIPO SALA',
#                 title=f'Promedio de Limpieza en {unidad} por Tipo de Sala',
#                 text='mean_cleanliness' if show_numbers else None,
#                 color_discrete_sequence=colors
#             )
#             if show_numbers:
#                 fig_unit.update_traces(texttemplate='%{text:.2f}', textposition='top center', mode='lines+markers+text')
#
#         else:
#             return "<p>Error: Tipo de gráfico no compatible.</p>"
#
#         # Update x-axis layout for cleaner period display
#         fig_unit.update_layout(
#             xaxis_title='Periodo',
#             yaxis_title='Promedio de Limpieza',
#             xaxis={'type': 'category'},
#         )
#
#         # Append the graph's HTML representation to the combined output
#         all_graphs_html += fig_unit.to_html(full_html=False)
#
#     return all_graphs_html

#-----------------------------------------------------------------------------------------------

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
        return "<p>Error: Columna 'UNIDAD HOSP.' no encontrada en los datos.</p>"

    # Convert 'FECHAHORA' to datetime
    elementos_df['FECHAHORA'] = pd.to_datetime(elementos_df['FECHAHORA'], errors='coerce')
    aseos_df['FECHAHORA'] = pd.to_datetime(aseos_df['FECHAHORA'], errors='coerce')

    # Drop rows with invalid dates and missing 'UNIDAD HOSP.' and make a copy to avoid SettingWithCopyWarning
    elementos_df = elementos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.']).copy()
    aseos_df = aseos_df.dropna(subset=['FECHAHORA', 'UNIDAD HOSP.']).copy()

    # Ensure 'UNIDAD HOSP.' is of type string
    elementos_df['UNIDAD HOSP.'] = elementos_df.loc[:, 'UNIDAD HOSP.'].astype(str)
    aseos_df['UNIDAD HOSP.'] = aseos_df.loc[:, 'UNIDAD HOSP.'].astype(str)

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

    # Group by period and hospital unit
    elementos_grouped = elementos_df.groupby(['Periodo', 'UNIDAD HOSP.'])['mean_cleanliness'].mean().reset_index()
    aseos_grouped = aseos_df.groupby(['Periodo', 'UNIDAD HOSP.'])['mean_cleanliness'].mean().reset_index()

    # Determine the color palette
    colors = COLOR_PALETTES.get(color_palette, px.colors.qualitative.Plotly)

    # Generate graph based on graph_type
    if graph_type == 'Bar Chart':
        fig_elementos = px.bar(
            elementos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            color='UNIDAD HOSP.',
            barmode='group',
            title='Promedio de Limpieza por Unidad Hospitalaria (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )
        fig_aseos = px.bar(
            aseos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            color='UNIDAD HOSP.',
            barmode='group',
            title='Promedio de Limpieza por Unidad Hospitalaria (Aseos)',
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
            color='UNIDAD HOSP.',
            title='Promedio de Limpieza por Unidad Hospitalaria (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )
        fig_aseos = px.line(
            aseos_grouped,
            x='Periodo',
            y='mean_cleanliness',
            color='UNIDAD HOSP.',
            title='Promedio de Limpieza por Unidad Hospitalaria (Aseos)',
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

    # Generate graphs by hospital unit and room type
    # Group by hospital unit, room type, and period to calculate the mean cleanliness
    elementos_grouped_tipo_sala = elementos_df.groupby(['Periodo', 'UNIDAD HOSP.', 'TIPO SALA'])['mean_cleanliness'].mean().reset_index()
    aseos_grouped_tipo_sala = aseos_df.groupby(['Periodo', 'UNIDAD HOSP.', 'TIPO SALA'])['mean_cleanliness'].mean().reset_index()

    # Iterate through each hospital unit and generate graphs for room types
    all_graphs_html = []
    for hospital_unit in elementos_grouped_tipo_sala['UNIDAD HOSP.'].unique():
        # Filter data for the specific hospital unit
        elementos_unit_df = elementos_grouped_tipo_sala[elementos_grouped_tipo_sala['UNIDAD HOSP.'] == hospital_unit]
        aseos_unit_df = aseos_grouped_tipo_sala[aseos_grouped_tipo_sala['UNIDAD HOSP.'] == hospital_unit]

        # Generate graphs for elements and bathrooms by room type
        fig_elementos_tipo_sala = px.bar(
            elementos_unit_df,
            x='Periodo',
            y='mean_cleanliness',
            color='TIPO SALA',
            barmode='group',
            title=f'Promedio de Limpieza por Tipo de Sala en {hospital_unit} (Elementos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )
        fig_aseos_tipo_sala = px.bar(
            aseos_unit_df,
            x='Periodo',
            y='mean_cleanliness',
            color='TIPO SALA',
            barmode='group',
            title=f'Promedio de Limpieza por Tipo de Sala en {hospital_unit} (Aseos)',
            text='mean_cleanliness' if show_numbers else None,
            color_discrete_sequence=colors
        )

        # Show numbers on graph if selected
        if show_numbers:
            fig_elementos_tipo_sala.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_aseos_tipo_sala.update_traces(texttemplate='%{text:.2f}', textposition='outside')

        # Update x-axis layout for cleaner period display
        fig_elementos_tipo_sala.update_layout(
            xaxis_title='Periodo',
            yaxis_title='Promedio de Limpieza',
            xaxis={'type': 'category'},
        )
        fig_aseos_tipo_sala.update_layout(
            xaxis_title='Periodo',
            yaxis_title='Promedio de Limpieza',
            xaxis={'type': 'category'},
        )

        # Append the graph's HTML representation to the list
        all_graphs_html.append(fig_elementos_tipo_sala.to_html(full_html=False))
        all_graphs_html.append(fig_aseos_tipo_sala.to_html(full_html=False))

    # Combine all graphs into one HTML output
    # Combine all graphs into one HTML output
    combined_html = graph_html + "".join(all_graphs_html)

    return combined_html
