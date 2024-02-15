import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from dash import callback_context
from dash.exceptions import PreventUpdate
import dash_table

# Cargar y preparar los datos
df_column = pd.read_csv("data/cazalla_de_la_sierra_adjusted.csv")
df = pd.read_csv("data/archivo_salida.csv")

df['fecha'] = pd.to_datetime(df['fecha'], format='%d-%m-%Y')
df['mes'] = df['fecha'].dt.month_name(locale='Spanish')  # Mes en español
df['semana'] = df['fecha'].dt.isocalendar().week
column_info = [{'Variable': col, 'Tipo de Dato': str(df_column[col].dtype)} for col in df_column.columns]

monthly_average = df.groupby('Month').mean()
normalized_monthly_average = monthly_average.apply(lambda x: (x - min_values[x.name]) / (max_values[x.name] - min_values[x.name]) if x.name in min_values else x)
normalized_monthly_average *= 5



def calcular_punto_medio(rango_str):
    limite_inferior, limite_superior = map(int, rango_str.split('-'))
    return (limite_inferior + limite_superior) / 2

df['var_strength_media'] = df['var_strength'].apply(calcular_punto_medio)

strength_mapping = {range_str: i for i, range_str in enumerate(df['var_strength'].unique())}
df['var_strength_numeric'] = df['var_strength'].apply(lambda x: strength_mapping[x])



# Inicializar la aplicación Dash
app = Dash(__name__)

# Meses iniciales para cada visualización
meses_iniciales = df['mes'].unique()[:4]





# Definir la estructura de la aplicación
app.layout = html.Div([
    html.Div([
    dash_table.DataTable(
        id='variable-info-table',
        columns=[{'name': i, 'id': i} for i in column_info[0].keys()],
        data=column_info,
        style_table={'height': '200px', 'overflowY': 'auto'}
        )
        ]
    )
] + [
    html.Div([
        dcc.Dropdown(
            id=f'mes-selector-{i}',
            options=[{'label': mes, 'value': mes} for mes in df['mes'].unique()],
            value=meses_iniciales[i],  # Valor por defecto para cada gráfico
        ),
        dcc.Graph(id=f'data-visualization-{i}')
    ], style={'width': '25%', 'display': 'inline-block'}) for i in range(2)  # Ajuste para polar
] + [
    html.Div([
        dcc.Graph(id='parallel-coordinates-visualization')
    ], style={'width': '50%', 'display': 'inline-block'})  # Ajuste para coordenadas paralelas

] + [
   html.Div([
        dcc.Dropdown(
            id='mes-selector-radar-1',
            options=[{'label': mes, 'value': mes} for mes in df['mes'].unique()],
            value=meses_iniciales[0]  # Valor inicial para el primer selector
        ),
        dcc.Dropdown(
            id='mes-selector-radar-2',
            options=[{'label': mes, 'value': mes} for mes in df['mes'].unique()],
            value=meses_iniciales[1] if len(meses_iniciales) > 1 else None  # Valor inicial para el segundo selector
        ),
        dcc.Graph(id='radar-chart')  # Espacio para el gráfico de radar
    ], style={'width': '50%', 'display': 'inline-block'})
] +[
    html.Div([
        dcc.Graph(id='weekly-comparison-bar-chart')  # Espacio para el gráfico de barras semanal
    ], style={'width': '50%', 'display': 'inline-block'})
])


# Callbacks para gráficos polar
for i in range(2):
    @app.callback(
        Output(f'data-visualization-{i}', 'figure'),
        [Input(f'mes-selector-{i}', 'value')]
    )
    def update_figure(selected_mes, i=i):
        filtered_df = df[df['mes'] == selected_mes]
        fig = px.bar_polar(filtered_df, r="var_frequency", theta="var_direction",
                           color="var_strength", template="plotly_dark",
                           color_discrete_sequence=px.colors.sequential.Plasma_r)
        return fig



# Callback para gráfico de coordenadas paralelas
@app.callback(
    Output('parallel-coordinates-visualization', 'figure'),
    [Input(f'mes-selector-{i}', 'value') for i in range(2)]
)

def update_parallel_coordinates(*args):
    ctx = callback_context

    # Verificar si el callback fue disparado y obtener el ID del input que lo disparó
    if not ctx.triggered:
        # En caso de que el callback no haya sido disparado por una acción del usuario,
        # podrías decidir usar un valor por defecto o manejar este caso como prefieras.
        selected_mes = args[0]  # Por ejemplo, usar el primer selector por defecto
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        selector_index = int(trigger_id.split('-')[-1])
        selected_mes = args[selector_index]

    filtered_df = df[df['mes'] == selected_mes]
    directions = filtered_df['var_direction'].unique()
    direction_mapping = {direction: i for i, direction in enumerate(directions)}
    direction_values = filtered_df['var_direction'].map(direction_mapping)

    fig = go.Figure(data=go.Parcoords(
        line=dict(color=filtered_df['var_strength_numeric'], colorscale='Tealrose'),
        dimensions=[
            dict(range=[filtered_df['var_frequency'].min(), filtered_df['var_frequency'].max()],
                 label='Frequency', values=filtered_df['var_frequency']),
            dict(range=[0, len(directions)-1],
                 tickvals=list(direction_mapping.values()),
                 label='Direction', values=direction_values,
                 ticktext=list(direction_mapping.keys())),
            dict(range=[filtered_df['var_strength_numeric'].min(), filtered_df['var_strength_numeric'].max()],
                 label='Strength', values=filtered_df['var_strength_numeric']),
            # Agregar var_temperature 
            dict(range=[filtered_df['var_temperature'].min(), filtered_df['var_temperature'].max()],
                    label='Temperature', values=filtered_df['var_temperature'])

        ]
    ))
    fig.update_layout(template="plotly_dark")
    return fig



@app.callback(
    Output('radar-chart', 'figure'),
    [Input('mes-selector-radar-1', 'value'),
     Input('mes-selector-radar-2', 'value')]
)

def update_radar_chart(mes1, mes2):
    if not mes1 or not mes2:
        raise PreventUpdate
    
    # Filtrar el DataFrame por los meses seleccionados
    df_mes1 = df[df['mes'] == mes1]
    df_mes2 = df[df['mes'] == mes2]
    
    # Calcular medias mensuales para cada variable de interés (ejemplo)
    medias_mes1 = [df_mes1['var_frequency'].mean(), df_mes1['var_strength_numeric'].mean(), df_mes1['var_temperature'].mean()/5]
    medias_mes2 = [df_mes2['var_frequency'].mean(), df_mes2['var_strength_numeric'].mean(), df_mes2['var_temperature'].mean()/5]

    # Categorías para el gráfico de radar
    categories = ['Frecuencia', 'Fuerza', 'Temperatura']

    # Crear el gráfico de radar
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
            r=medias_mes1,
            theta=categories,
            fill='toself',
            name=mes1
        ))
    
    fig.add_trace(go.Scatterpolar(
            r=medias_mes2,
            theta=categories,
            fill='toself',
            name=mes2
        ))
    
    # Configuración adicional del gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]  # Ajustar según tus datos
            )),
        showlegend=True
    )
    fig.update_layout(template="plotly_dark")
    return fig

def update_radar_chart_with_temperature(mes1, mes2):
    if not mes1 or not mes2:
        raise PreventUpdate
    
    # Filtrar el DataFrame por los meses seleccionados
    df_mes1 = df[df['mes'] == mes1]
    df_mes2 = df[df['mes'] == mes2]
    
    # Calcular medias mensuales para cada variable de interés (ejemplo)
    medias_mes1 = [df_mes1['var_frequency'].mean(), df_mes1['var_strength_numeric'].mean(), df_mes1['var_temperature'].mean()/5]
    medias_mes2 = [df_mes2['var_frequency'].mean(), df_mes2['var_strength_numeric'].mean(), df_mes2['var_temperature'].mean()/5]

    # Categorías para el gráfico de radar
    categories = ['Frecuencia', 'Fuerza', 'Temperatura']

    # Crear el gráfico de radar
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
            r=medias_mes1,
            theta=categories,
            fill='toself',
            name=mes1
        ))
    
    fig.add_trace(go.Scatterpolar(
            r=medias_mes2,
            theta=categories,
            fill='toself',
            name=mes2
        ))
    
    # Configuración adicional del gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]  # Ajustar según tus datos
            )),
        showlegend=True
    )
    fig.update_layout(template="plotly_dark")
    return fig
    

@app.callback(
    Output('weekly-comparison-bar-chart', 'figure'),
    [Input('mes-selector-radar-1', 'value'),
     Input('mes-selector-radar-2', 'value')]
)

def update_weekly_bar_chart(mes1, mes2):
    if not mes1 or not mes2:
        raise PreventUpdate
    
    # Preparar los datos para el gráfico de barras
    df_filtered = df[df['mes'].isin([mes1, mes2])]
    weekly_means = df_filtered.groupby(['mes', 'semana'])[['var_frequency', 'var_strength_media']].mean().reset_index()

    # Aquí, suponemos que quieres comparar 'var_frequency' como ejemplo
    data = []
    for mes in [mes1, mes2]:
        df_temp = weekly_means[weekly_means['mes'] == mes]
        data.append(go.Bar(
            x=df_temp['semana'],
            y=df_temp['var_frequency'],  # Ajusta esto a la variable que quieras comparar
            name=mes
        ))
    
    # Configurar el layout del gráfico de barras
    layout = go.Layout(
        title='Comparación Semanal de Frecuencia',  # Ajusta el título según sea necesario
        xaxis={'title': 'Semana'},
        yaxis={'title': 'Frecuencia Media'},  # Ajusta según la variable de interés
        barmode='group',
        template="plotly_dark"
    )
    
    return {'data': data, 'layout': layout}


# Correr la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)