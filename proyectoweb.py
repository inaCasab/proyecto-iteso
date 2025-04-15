# Importación de librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Carga del archivo CSV en un DataFrame
df = pd.read_csv("netflix_users.csv")

# Mostrar el contenido del DataFrame
st.dataframe(df)
df.info()

# Definir la columna como índice del DataFrame
st.write(df.columns)
df.set_index("Name", inplace=True)
# Mostrar el contenido del DataFrame con el nuevo índice
st.dataframe(df)

# Homogeneizar los nombres de las columnas
df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

# Mostrar el contenido del DataFrame con los nuevos nombres de columna
st.dataframe(df)

# Valores nulos en cada columna
null_counts = df.isnull().sum()

# Total de valores nulos en todo el DataFrame
total_nulls = null_counts.sum()

st.write(f"Total de celdas con valores nulos: {total_nulls}")

# Mostrar los nombres de las categorías
st.write(df.columns)

# Seleccionar la media de edad de usuarios
columna = "age"

# Calcular la media
media_valor = df[columna].mean()

# Imprimir el resultado
st.write(f"La media de la columna '{columna}' es: {media_valor}")

# Contar usuarios por país y mostrar los 5 más comunes
usuarios_por_pais = df['country'].value_counts().head(5)
st.write("Top 5 países con más usuarios:")
st.write(usuarios_por_pais)

# Contar usuarios por país y seleccionar los 5 con mayor cantidad
usuarios_mayor_pais = df['country'].value_counts().head(5)

# Crear el histograma
plt.figure(figsize=(8, 5))
usuarios_mayor_pais.plot(kind='bar', color='royalblue')
plt.title('Top 5 países con más usuarios en Netflix')
plt.xlabel('País')
plt.ylabel('Cantidad de usuarios')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--')
# Mostrar el gráfico en Streamlit
st.pyplot(plt)

# Contar usuarios por país y mostrar los 5 con menor cantidad
usuarios_menor_pais = df['country'].value_counts().tail(5)
st.write("Países con menor cantidad de usuarios:")
st.write(usuarios_menor_pais)

# Crear el histograma
plt.figure(figsize=(8, 5))
usuarios_menor_pais.plot(kind='bar', color='salmon')
plt.title('Países con menor cantidad de usuarios en Netflix')
plt.xlabel('País')
plt.ylabel('Cantidad de usuarios')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--')
# Mostrar el gráfico en Streamlit
st.pyplot(plt)

# Crear rangos de horas de visualización
bins = [0, 5, 10, 15, 20, 25, 30, 50]  # Definir los intervalos
labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '30+']  # Etiquetas de los intervalos

# Agrupar los datos en los intervalos definidos
df['watch_time_hours'] = pd.cut(df['watch_time_hours'], bins=bins, labels=labels, right=False)

# Contar la cantidad de usuarios en cada intervalo
tabla_horas = df['watch_time_hours'].value_counts().sort_index()

# Convertir en DataFrame para mejor visualización
tabla_horas_df = pd.DataFrame({'Rango de horas semanales': labels, 'Cantidad de usuarios': tabla_horas.values})

# Mostrar la tabla
st.write(tabla_horas_df)