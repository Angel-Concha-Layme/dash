import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from dash import callback_context
from dash.exceptions import PreventUpdate
from dash import dash_table
import openai


# Carga los datos
df = pd.read_csv('data/2015_2017_preprocesado.csv')
df_short = pd.read_csv('data/2015_2017_short.csv')

df['Date'] = pd.to_datetime(df['Date'])
df_short['Date'] = pd.to_datetime(df_short['Date'])
df['Month'] = df['Date'].dt.month_name(locale='English')

## Variables para los gráficos polar
meses_iniciales = df['Month'].unique()[:2]

def calculate_temperature_range(temp):
    # Ajustar el mínimo y máximo para que encajen en los rangos definidos
    min_temp = 10  # Mínimo ajustado para el cálculo del rango
    # Encontrar el rango inferior múltiplo de 2 más cercano hacia abajo
    range_start = 2 * ((temp - min_temp) // 2) + min_temp
    # El rango superior es simplemente 2 grados más
    range_end = range_start + 2
    return f"{range_start}-{range_end}"

df['Temperature_range'] = df['Temperature'].apply(calculate_temperature_range)


# Variables de configuración de color
v_theme = "plotly_dark"
v_color = "white"


# Analisis de datos con openai
openai.api_key = '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'

def analizar_contenido_columnas(df):
    # Preparar estadísticas del dataframe para incluir en el prompt
    descripcion_estadisticas = ""
    for col in df.columns:
        descripcion_estadisticas += f"{col}: Max={df[col].max()}, Min={df[col].min()}, Media={df[col].mean()}, Desviación Estándar={df[col].std()}\n"
    
    # Inicializar la descripción de las columnas con un ejemplo de valor
    descripcion_columnas = "\n".join([f"- {col}: {df[col].iloc[0]} (Ejemplo de valor)" for col in df.columns])
    
    prompt = f"""Dado un conjunto de datos sobre condiciones ambientales y mediciones, con las siguientes columnas y un ejemplo de valor para cada una, además de estadísticas clave como el valor máximo, mínimo, la media y la desviación estándar, infiere el tipo de información que podría contener cada columna y cómo se podría utilizar. Por favor, proporciona tus inferencias en el formato "Nombre de Columna: Descripción", donde cada descripción debe ser concisa y clara.

Columnas y ejemplos de valores:
{descripcion_columnas}

Estadísticas de las columnas:
{descripcion_estadisticas}

Para cada columna, describe brevemente el tipo de datos o información que representa, utilizando el formato "Nombre de Columna @: Descripción" (es MUY IMPORTANTE que uses los dos puntos "@:" para separar el nombre y la descripción). Por ejemplo:
- Date @: Representa la fecha de la medición en formato YYYY-MM-DD. Rango de fechas desde 2015-01-01 hasta 2017-12-31.
- Temperature @: Temperatura del aire en grados Celsius. Valores desde -5.2°C a 35.1°C. Media de 18.3°C y desviación estándar de 5.2°C.
- Wind_velocity @: Velocidad del viento en metros por segundo. Valores desde 0.2 m/s a 10.3 m/s. Media de 3.1 m/s y desviación estándar de 1.2 m/s.

Es crucial que sigas este formato sin excepciones para cada descripción."""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu tarea es analizar las siguientes columnas de un conjunto de datos y proporcionar inferencias sobre el tipo de información que cada una podría contener, utilizando el formato específico requerido."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1024,  # Ajusta esto según la longitud esperada de la respuesta
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].message['content'].strip()


respuesta_api_local ="""Date @: Representa la fecha y hora de cada medición en formato YYYY-MM-DD HH:MM:SS. El rango de fechas va desde 2015-05-07 hasta 2015-05-20, con una media en 2015-05-13 y una desviación estándar de aproximadamente 5 días.
Concentration @: Esta columna representa la concentración de algún componente no especificado en el aire, posiblemente un contaminante. Los valores oscilan entre 14.76 y 32.79 con una media de 19.75 y una desviación estándar de 6.63.
Precipitation @: Mide la cantidad de precipitación en algún formato no especificado, posiblemente en milímetros. Los valores van de 0.0 a 0.1, con una media de 0.016 y una desviación estándar de 0.041.
Wind_velocity @: Representa la velocidad del viento en una unidad no especificada, probablemente metros por segundo. Los valores van desde 0.67 hasta 2.4, con una media de 1.42 y una desviación estándar de 0.68.
Wind_direction @: Representa la dirección del viento en grados, con 0 representando el norte y aumentando en el sentido de las agujas del reloj. Los valores van desde 6.0 a 18.0, con una media de 11.17 y una desviación estándar de 4.47.
Temperature @: Representa la temperatura ambiental en grados Celsius. Los valores oscilan entre 16.85°C y 18.41°C, con una media de 17.53°C y una desviación estándar de 0.59°C.
Humidity @: Representa la humedad relativa del ambiente en porcentaje. Los valores varían entre 70.0% y 79.5%, con una media de 75.14% y una desviación estándar de 4.27%."""

print(respuesta_api_local)

#respuesta_api = analizar_contenido_columnas(df_short)
#print(respuesta_api)

# Procesando la respuesta para separar en claves y valores
claves = []
valores = []
for linea in respuesta_api_local.split('\n'):
    clave, valor = linea.split('@:')
    claves.append(clave)
    valores.append(valor)

# Definir colores en modo oscuro para la tabla
color_fondo = '#303030'  
color_texto = '#FFFFFF'  
color_celda = '#434343' 
color_encabezado = '#2C2C2C'

table_api = go.Figure(data=[go.Table(
    header=dict(
        values=['Variable', 'Descripción'],
        line_color=color_fondo,
        fill_color=color_encabezado,
        align='left',
        font=dict(color=color_texto, size=16)
    ),
    cells=dict(
        values=[claves, valores],
        line_color=color_fondo,
        fill_color=[color_celda, color_celda],
        align='left',
        font=dict(color=color_texto, size=14),
        height=30
    )
)],
layout=go.Layout(
    title=dict(
        text="Description of variables with Artificial Intelligence",
        x=0.5,
        xanchor='center',
        y=0.95,
        font=dict(size=24, color=color_texto)
    ),
    margin=dict(t=60, l=10, r=10, b=10),
    template=v_theme
))



####-------------------------------------------------------####
####--------------------- GLOBAL VIEW ---------------------####
####-------------------------------------------------------####

# Crea una figura con Plotly Express
fig = px.scatter(df, x="Date", y="Concentration",
                 size="Concentration", color="Seasons",
                 hover_data={
                     "Date": True,
                     "Precipitation": True,
                     "Temperature": True,
                     "Wind_velocity": True,
                     "Wind_direction": True,
                     "Humidity": True
                 },
                 labels={
                     "Date ": "Date",
                     "Seasons ": "Season",
                     "Concentration ": "Concentration (ug/m³) ",
                     "Precipitation ": "Precipitation (mm) ",
                     "Temperature ": "Temperature (°C) ",
                     "Wind_velocity ": "Wind Velocity (m/s) ",
                     "Wind_direction ": "Wind Direction (°) ",
                     "Humidity ": "Humidity (%) ",
                 },
                 template=v_theme)

# Agrega labels a las variables
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="PM10 concentration (µg/m³)",
    title=dict( text= "Global view", x=0.5, y=0.95),
    legend_title="Season of the year",
    font=dict(
        family="Arial",
        size=16,
        color=v_color
    )
)

# Ajusta las marcas del eje X para mostrar cada mes
fig.update_xaxes(
    tickformat="%b %Y",
    tickmode='auto',
    nticks=len(df['Date'].dt.to_period('M').unique())
)


####-------------------------------------------------------####
####----------------------- WIND VIEW ---------------------####
####-------------------------------------------------------####

fig_wind = px.bar_polar(df, r="Wind_velocity", theta="Wind_direction_cardinality",
                        color="Temperature_range",  # O cualquier otra columna para color
                        hover_data=["Wind_velocity", "Wind_direction_cardinality", "Temperature"],
                        labels={
                            "Wind_velocity": "Wind Velocity (m/s)",
                            "Wind_direction_cardinality": "Wind Direction (°)",
                            "Temperature": "Temperature (°C)"
                        },
                        template=v_theme)




####-------------------------------------------------------####
####-------------- PARALLEL COORDINATES VIEW --------------####
####-------------------------------------------------------####

fig_parallel = px.parallel_coordinates(df, color="Concentration",
                                        dimensions=["Concentration", "Temperature", "Wind_velocity", "Humidity", "Precipitation"],
                                        labels={
                                            "Concentration": "Concentration (µg/m³)",
                                            "Temperature": "Temperature (°C)",
                                            "Wind_velocity": "Wind Velocity (m/s)",
                                            "Humidity": "Humidity (%)",
                                            "Precipitation": "Precipitation (mm)"
                                        },
                                        color_continuous_scale=px.colors.diverging.Tealrose,
                                        template=v_theme)



####-------------------------------------------------------####
####--------------------- RADAR CHART VIEW ----------------####
####-------------------------------------------------------####

#Calcular promedios mensuales para variables de interés
variables_of_interest = ['Concentration', 'Precipitation', 'Wind_velocity', 'Wind_direction', 'Temperature', 'Humidity']
monthly_averages_full = df.groupby('Month')[variables_of_interest].mean()

# Normalizar los promedios mensuales basándose en valores máximos y mínimos del DataFrame completo
max_values_full = df[variables_of_interest].max()
min_values_full = df[variables_of_interest].min()

normalized_data_full = (monthly_averages_full - min_values_full) / (max_values_full - min_values_full)

normalized_data_full *= 5


####-------------------------------------------------------####
####------------------ GROUPED BAR CHART ------------------####
####-------------------------------------------------------####





####-------------------------------------------------------####
####--------------------- DASH APPLICATION ----------------####
####-------------------------------------------------------####

# Inicializa la aplicación Dash
app = dash.Dash(__name__)

# Define el layout de la aplicación
app.layout = html.Div([
    dcc.Graph(
        id='table-api',
        figure=table_api,
        style={'width': '50%', 'display': 'inline-block'}
    ),
    dcc.Graph(
        id='bubble-chart',
        figure=fig,
        style={'width': '50%', 'display': 'inline-block'}
    )
    
] + [
    html.Div([
        dcc.Dropdown(
            id=f'wind-mes-selector-{i}',
            options=[{'label': month, 'value': month} for month in df['Month'].unique()],
            value=df['Month'].unique()[0]  # Asume que df['Month'] contiene los meses
        ),
        dcc.Graph(id=f'wind-view-chart-{i}')
    ], style={'width': '25%', 'display': 'inline-block'}) for i in range(2)  # Dos gráficos de Wind View
] + [
    dcc.Graph(
        id='parallel-coordinates-chart',
        figure=fig_parallel,
        style={'width': '50%', 'display': 'inline-block'}
    ),
    dcc.Graph(
        id='radar-chart',
        style={'width': '50%', 'display': 'inline-block'}
    )
] + [
    html.Div([
        dcc.Dropdown(
        id='variable-selector',
        options=[{'label': variable, 'value': variable} for variable in ['Concentration', 'Precipitation', 'Wind_velocity', 'Wind_direction', 'Temperature', 'Humidity']],
        value='Concentration',  # Valor predeterminado
        ),
        dcc.Graph(id='grouped-bar-chart'),
    ], style={'width': '50%', 'display': 'inline-block'}
    )

] + [
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'scroll'},
            style_cell={
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal',
                'fontSize': '18',
            },
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_data_conditional=[
                {
                    'if': {
                        'state': 'active'  # Selecciona la fila activa
                    },
                    'backgroundColor': 'rgba(0, 116, 217, 0.3)',
                    'border': '1px solid rgb(0, 116, 217)',
                    'color': 'darkslategray'
                }
            ]
        )
    ])
]
)


# Callbacks para wind view
for i in range(2):
    @app.callback(
        Output(f'wind-view-chart-{i}', 'figure'),
        [Input(f'wind-mes-selector-{i}', 'value')]
    )
    def update_wind_view(selected_mes, i=i):
        # Filtra df por el mes seleccionado
        filtered_df = df[df['Month'] == selected_mes]
        # Crea la figura de bar_polar para Wind View con los datos filtrados
        fig_wind = px.bar_polar(filtered_df, r="Wind_velocity", theta="Wind_direction_cardinality",
                                color="Temperature_range",  # O cualquier otra columna para color
                                hover_data=["Wind_velocity", "Wind_direction_cardinality", "Temperature"],
                                labels={
                                    "Wind_velocity": "Wind Velocity (m/s)",
                                    "Wind_direction_cardinality": "Wind Direction (°)",
                                    "Temperature": "Temperature (°C)"
                                },
                                template=v_theme)
        
        # Personaliza la figura si es necesario
        fig_wind.update_layout(
            title= dict( text= f"Wind View (Selected Month: {selected_mes})", x=0.5, y=0.95),
            font=dict(
                family="Arial",
                size=16,
                color=v_color
            )
        )
        
        return fig_wind


# Callbacks para Parallel Coordinates View (se selecciona el mismo mes en ambos gráficos)
@app.callback(
    Output('parallel-coordinates-chart', 'figure'),
    [Input(f'wind-mes-selector-{i}', 'value') for i in range(2)]
)
def update_parallel_coordinates(selected_mes_1, selected_mes_2):
    # Determina cuál input fue el que cambió
    ctx = callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Filtra df basado en el input que cambió
    if trigger_id == 'wind-mes-selector-0':
        filtered_df = df[df['Month'] == selected_mes_1]
    else:
        filtered_df = df[df['Month'] == selected_mes_2]

    mes_selected = selected_mes_1 if trigger_id == 'wind-mes-selector-0' else selected_mes_2
    # Crea la figura de coordenadas paralelas con los datos filtrados
    fig_parallel = px.parallel_coordinates(filtered_df, color="Concentration",
                                          dimensions=["Concentration", "Temperature", "Wind_velocity", "Humidity", "Precipitation"],
                                          labels={
                                              "Concentration": "Concentration (µg/m³)",
                                              "Temperature": "Temperature (°C)",
                                              "Wind_velocity": "Wind Velocity (m/s)",
                                              "Humidity": "Humidity (%)",
                                              "Precipitation": "Precipitation (mm)"
                                          },
                                          color_continuous_scale=px.colors.diverging.Tealrose,
                                          template=v_theme)

    # Actualiza el layout de la figura si es necesario
    fig_parallel.update_layout(
        margin=dict(t=100),
        title=dict(text=f"Parallel Coordinates View (Filtered by Selected Month: {mes_selected})", x=0.5, y=0.95),
        font=dict(
            family="Arial",
            size=16,
            color=v_color
        ),
    )

    return fig_parallel


# Callbacks para Radar Chart View
@app.callback(
    Output('radar-chart', 'figure'),
    [Input(f'wind-mes-selector-{i}', 'value') for i in range(2)]
)

def update_radar_chart(selected_mes_1, selected_mes_2):
    variables_of_interest = ['Concentration', 'Precipitation', 'Wind_velocity', 'Wind_direction', 'Temperature', 'Humidity']
    monthly_averages_full = df.groupby('Month')[variables_of_interest].mean()

    # Normalizar los promedios mensuales basándose en valores máximos y mínimos del DataFrame completo
    max_values_full = df[variables_of_interest].max()
    min_values_full = df[variables_of_interest].min()

    normalized_data_full = (monthly_averages_full - min_values_full) / (max_values_full - min_values_full)
    normalized_data_full *= 5
    
    # Filtrar el DataFrame por los meses seleccionados
    filtered_df_1 = df[df['Month'] == selected_mes_1]
    filtered_df_2 = df[df['Month'] == selected_mes_2]
    
    # Calcular los promedios mensuales para cada mes seleccionado
    monthly_averages_1 = filtered_df_1[variables_of_interest].mean()
    monthly_averages_2 = filtered_df_2[variables_of_interest].mean()
    
    # Normalizar los promedios mensuales
    normalized_data_1 = (monthly_averages_1 - min_values_full) / (max_values_full - min_values_full) * 5
    normalized_data_2 = (monthly_averages_2 - min_values_full) / (max_values_full - min_values_full) * 5
    
    # Crea la figura de radar chart con los datos filtrados
    fig_radar = go.Figure()
    
    # Añadir los datos al radar chart para cada mes seleccionado
    fig_radar.add_trace(go.Scatterpolar(
        r=normalized_data_1.values,
        theta=variables_of_interest,
        fill='toself',
        name=f'Month {selected_mes_1}'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=normalized_data_2.values,
        theta=variables_of_interest,
        fill='toself',
        name=f'Month {selected_mes_2}'
    ))

    # Actualizar el layout de la figura si es necesario
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        title=dict(text="Radar Chart View", x=0.5, y=0.95),
        font=dict(
            family="Arial",
            size=16,
            color=v_color
        ),
        template=v_theme
    )

    return fig_radar


# Callbacks para Grouped Bar Chart 
@app.callback(
    Output('grouped-bar-chart', 'figure'),
    [Input(f'wind-mes-selector-{i}', 'value') for i in range(2)] +
    [Input('variable-selector', 'value')]
)

def update_grouped_bar_chart(selected_mes_1, selected_mes_2, selected_variable):
    # Filtrar el DataFrame por los meses seleccionados y seleccionar la variable de interés
    filtered_df_1 = df[df['Month'] == selected_mes_1]
    filtered_df_2 = df[df['Month'] == selected_mes_2]

    # Asumiendo que tienes una columna 'Week' que indica la semana del mes
    weekly_averages_1 = filtered_df_1.groupby('Week')[selected_variable].mean()
    weekly_averages_2 = filtered_df_2.groupby('Week')[selected_variable].mean()

    weeks = weekly_averages_1.index  # Asumiendo que ambas selecciones tienen las mismas semanas

    # Crear la figura de Plotly con datos de barras agrupadas
    fig = go.Figure(data=[
        go.Bar(name=f'Month {selected_mes_1}', x=weeks, y=weekly_averages_1),
        go.Bar(name=f'Month {selected_mes_2}', x=weeks, y=weekly_averages_2)
    ])

    # Cambiar el modo de barra a 'group' para agruparlas
    fig.update_layout(
        barmode='group',
        title=f'Weekly Comparison of {selected_variable}',
        xaxis_title='Semana',
        yaxis_title=selected_variable,
        legend_title='Mes',
        font=dict(
            family="Arial",
            size=16,
            color=v_color
        ),
        template=v_theme
    )

    return fig


# Ejecuta la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
