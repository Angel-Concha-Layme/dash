import pandas as pd
from datetime import datetime

# ------------------------------------------#
###    PREPROCESAMIENTO DE LOS DATOS      ###
# ------------------------------------------#

pd.set_option('display.max_columns', None)

# Cargar el dataset
file_path = 'data/2015_2017.tsv'
data = pd.read_csv(file_path, sep='\t')



# Convertir la columna 'Data' al formato de fecha
data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')

data.to_csv('2015_2017_short.csv', index=False)

# Valores máximos y mínimos de las variables
maximos = data.max(numeric_only=True)
minimos = data.min(numeric_only=True)

# Distribución de las variables (media y desviación estándar)
distribucion = data.describe().loc[['mean', 'std']]

# Mostrar valores máximos y mínimos, y la distribución
print('Valores máximos:')
print(maximos)
print('Valores mínimos:')
print(minimos)
print('Distribución:')
print(distribucion)


# Guardar el dataset preprocesado
#data.to_csv('2015_2017_short.csv', index=False)