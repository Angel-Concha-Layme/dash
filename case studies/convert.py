import pandas as pd
import numpy as np

# Función para asignar temperaturas aleatorias entre 1 y 18 (enteros) para cualquier fecha
def asignar_temperatura_aleatoria(fecha):
    return np.random.randint(1, 19)

# Lee el archivo CSV
archivo_csv = "data/data1.csv"
df = pd.read_csv(archivo_csv)

# Aplica la nueva función a cada fila del DataFrame para asignar temperaturas aleatorias
df['var_temperature'] = df['fecha'].apply(asignar_temperatura_aleatoria)

# Guarda el DataFrame modificado en un nuevo archivo CSV
df.to_csv("archivo_salida.csv", index=False)
