
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from dash import callback_context

# Cargar y preparar los datos
df = pd.read_csv("data/cazalla_de_la_sierra_adjusted.csv")
df['fecha'] = pd.to_datetime(df['fecha'], format='%d-%m-%Y')
df['mes'] = df['fecha'].dt.month_name(locale='Spanish')  # Mes en español
df['semana'] = df['fecha'].dt.isocalendar().week


strength_mapping = {range_str: i for i, range_str in enumerate(df['var_strength'].unique())}
df['var_strength_numeric'] = df['var_strength'].apply(lambda x: strength_mapping[x])


# Inicializar la aplicación Dash
app = Dash(__name__)

# Meses iniciales para cada visualización
meses_iniciales = df['mes'].unique()[:4]

# Definir la estructura de la aplicación
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id=f'mes-selector-{i}',
            options=[{'label': mes, 'value': mes} for mes in df['mes'].unique()],
            value=meses_iniciales[i],  # Valor por defecto para cada gráfico
        ),
        dcc.Graph(id=f'data-visualization-{i}')
    ], style={'width': '25%', 'display': 'inline-block'}) for i in range(4)  # Ajuste para polar
] + [
    html.Div([
        dcc.Graph(id='parallel-coordinates-visualization')
    ], style={'width': '50%', 'display': 'block'})  # Ajuste para coordenadas paralelas
])


# Callbacks para gráficos polar
for i in range(4):
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
    [Input(f'mes-selector-{i}', 'value') for i in range(4)]
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
                 label='Strength', values=filtered_df['var_strength_numeric'])
        ]
    ))
    fig.update_layout(template="plotly_dark")
    return fig

# Correr la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
"""

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True)

"""