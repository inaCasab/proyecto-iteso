import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Carga del archivo CSV en un DataFrame
df = pd.read_csv("netflix_users.csv")

# Configuración de la página
st.set_page_config(page_title="Netflix Users Data", page_icon="📊", layout="wide")

# Agregar una imagen al inicio de la app
st.image('Netflix.jpg', caption='Netflix Users Data', use_column_width=True)

# Título y descripción
st.title('Análisis de Datos de Usuarios de Netflix')
st.subheader('Explora los insights de los usuarios de Netflix')

# Mostrar el contenido del DataFrame
st.dataframe(df)
df.info()

# Filtros interactivos en la barra lateral
st.sidebar.header("Filtros")
pais_seleccionado = st.sidebar.selectbox('Selecciona un país', df['country'].unique())
edad_minima = st.sidebar.slider('Edad mínima', min_value=int(df['age'].min()), max_value=int(df['age'].max()), value=20)

# Filtrar los datos según los filtros aplicados
df_filtrado = df[(df['country'] == pais_seleccionado) & (df['age'] >= edad_minima)]

# Mostrar los datos filtrados
st.write(f"Datos filtrados por país: {pais_seleccionado} y edad mayor o igual a {edad_minima}")
st.dataframe(df_filtrado)

# Definir la columna como índice del DataFrame
df.set_index("Name", inplace=True)

# Homogeneizar los nombres de las columnas
df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

# Mostrar el contenido del DataFrame con los nuevos nombres de columna
st.write("DataFrame con nombres de columnas homogéneos:")
st.dataframe(df)

# Valores nulos en cada columna
null_counts = df.isnull().sum()

# Total de valores nulos en todo el DataFrame
total_nulls = null_counts.sum()
st.write(f"Total de celdas con valores nulos: {total_nulls}")

# Análisis 1: Edad promedio por país
edad_promedio_por_pais = df.groupby('country')['age'].mean().sort_values(ascending=False)
fig1 = px.bar(edad_promedio_por_pais, x=edad_promedio_por_pais.index, y=edad_promedio_por_pais.values,
              labels={'x': 'País', 'y': 'Edad Promedio'}, title="Edad Promedio de Usuarios por País")
st.plotly_chart(fig1)

# Análisis 2: Correlación entre edad y horas de visualización
correlacion = df[['age', 'watch_time_hours']].corr()
st.write(f"La correlación entre edad y horas de visualización es: {correlacion.iloc[0, 1]}")

fig2 = px.scatter(df, x='age', y='watch_time_hours', color='country', title="Correlación entre Edad y Horas de Visualización")
st.plotly_chart(fig2)

# Análisis 3: Distribución de usuarios por género
if 'gender' in df.columns:
    usuarios_por_genero = df['gender'].value_counts()
    fig3 = px.pie(usuarios_por_genero, names=usuarios_por_genero.index, values=usuarios_por_genero.values,
                  title="Distribución de Usuarios por Género")
    st.plotly_chart(fig3)

# Contar usuarios por país y mostrar los 5 más comunes
usuarios_por_pais = df['country'].value_counts().head(5)
st.write("Top 5 países con más usuarios:")
st.write(usuarios_por_pais)

# Gráfico interactivo con Plotly para los 5 países con más usuarios
fig4 = px.bar(usuarios_por_pais, x=usuarios_por_pais.index, y=usuarios_por_pais.values,
              labels={'x': 'País', 'y': 'Usuarios'}, title="Top 5 países con más usuarios")
st.plotly_chart(fig4)

# Contar usuarios por país y mostrar los 5 con menor cantidad
usuarios_menor_pais = df['country'].value_counts().tail(5)
st.write("Países con menor cantidad de usuarios:")
st.write(usuarios_menor_pais)

# Gráfico interactivo con Plotly para los 5 países con menos usuarios
fig5 = px.bar(usuarios_menor_pais, x=usuarios_menor_pais.index, y=usuarios_menor_pais.values,
              labels={'x': 'País', 'y': 'Usuarios'}, title="Países con Menos Usuarios")
st.plotly_chart(fig5)

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