import pandas as pd
from datetime import datetime

# ------------------------------------------#
###    PREPROCESAMIENTO DE LOS DATOS      ###
# ------------------------------------------#

pd.set_option('display.max_columns', None)

# Cargar el dataset
file_path = 'data/2015_2017.tsv'
data = pd.read_csv(file_path, sep='\t')

data.to_csv('2015_2017_short.csv', index=False)


# Convertir la columna 'Data' al formato de fecha
data['Data'] = pd.to_datetime(data['Data'], format='%m/%d/%Y')


# Extraer el mes y la semana
data['Month'] = data['Data'].dt.month
data['Week'] = data['Data'].dt.isocalendar().week

# Función para convertir la dirección del viento en grados a puntos cardinales
def direccion_viento(grados):
    direcciones = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    indice = int((grados + 22.5) // 45)
    return direcciones[indice % 8]

# Agregar la columna de dirección del viento en puntos cardinales
data['Wind_direction_cardinality'] = data['Wind_direction'].apply(direccion_viento)
     
# Valores máximos y mínimos de las variables
maximos = data.max(numeric_only=True)
minimos = data.min(numeric_only=True)

# Distribución de las variables (media y desviación estándar)
distribucion = data.describe().loc[['mean', 'std']]

# Crear dataframes por año
data['Year'] = data['Data'].dt.year
dataframes_por_año = {año: datos for año, datos in data.groupby('Year')}

# Mostrar valores máximos y mínimos, y la distribución
print('Valores máximos:')
print(maximos)
print('\nValores mínimos:')
print(minimos)
print('\nDistribución:')
print(distribucion)


# Agregar estaciones del año
# Verano: Desde el 21 de diciembre hasta el 20 de marzo
# Otoño: Desde el 21 de marzo hasta el 20 de junio
# Invierno: Desde el 21 de junio hasta el 20 de septiembre
# Primavera: Desde el 21 de septiembre hasta el 20 de diciembre

# Función para determinar la estación del año
def estacion_hemisferio_sur(mes, dia):
    if (mes > 3 and mes < 6) or (mes == 3 and dia >= 21) or (mes == 6 and dia < 21):
        return 'Fall'
    elif (mes > 6 and mes < 9) or (mes == 6 and dia >= 21) or (mes == 9 and dia < 21):
        return 'Winter'
    elif (mes > 9 and mes < 12) or (mes == 9 and dia >= 21) or (mes == 12 and dia < 21):
        return 'Spring'
    else:
        return 'Summer'
    
# Aplicar la función para agregar la columna 'Estacion'
data['Seasons'] = data.apply(lambda row: estacion_hemisferio_sur(row['Month'], row['Data'].day), axis=1)

# Mostrar las primeras filas para verificar la nueva columna
print(data.head(5))

# Guardar el dataset preprocesado
#data.to_csv('2015_2017_short.csv', index=False)