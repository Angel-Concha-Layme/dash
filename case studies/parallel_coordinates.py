"""
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

# Cargando el conjunto de datos de iris
df = px.data.iris()

# Creando la figura de coordenadas paralelas
def create_figure():
    return px.parallel_coordinates(
        df,
        color="species_id",
        labels={
            "species_id": "Species",
            "sepal_width": "Sepal Width",
            "sepal_length": "Sepal Length",
            "petal_width": "Petal Width",
            "petal_length": "Petal Length",
        },
        color_continuous_scale=px.colors.diverging.Tealrose,
        color_continuous_midpoint=2
    )

# Inicializando la aplicación Dash
app = Dash(__name__)

# Definiendo el layout de la aplicación
app.layout = html.Div([
    html.H1(children='Iris Dataset Visualization', style={'textAlign': 'center'}),
    dcc.Graph(figure=create_figure(), id='parallel-coordinates-plot')
])

# Ejecutando la aplicación
if __name__ == '__main__':
    app.run(debug=True)

"""

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Cargar datos
df = px.data.iris()

# Inicializar la aplicación Dash
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Iris Dataset: Interactive Visualizations", style={'textAlign': 'center'}),
    dcc.Graph(id='scatter-plot', figure=px.scatter(df, x='sepal_length', y='sepal_width', color='species')),
    dcc.Graph(id='bar-plot')
])

# Callbacks para interactividad
@app.callback(
    Output('bar-plot', 'figure'),
    [Input('scatter-plot', 'clickData')]
)
def update_bar_plot(clickData):
    if clickData is None:
        return px.bar(df, x='species', y='petal_length', title='Petal Length by Species')
    else:
        point_index = clickData['points'][0]['pointIndex']
        selected_species = df.iloc[point_index]['species']
        filtered_df = df[df['species'] == selected_species]
        return px.bar(filtered_df, x='species', y='petal_length', title=f'Petal Length for {selected_species}')

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
