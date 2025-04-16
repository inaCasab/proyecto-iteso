import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# Cargar el archivo CSV
df = pd.read_csv("netflix_users.csv")
df = df.rename(columns={
    "User_ID": "ID_Usuario",
    "Name": "Nombre",
    "Age": "Edad",
    "Country": "País",
    "Subscription_Type": "Tipo_Suscripción",
    "Watch_Time_Hours": "Horas_Vistas",
    "Favorite_Genre": "Género_Favorito",
    "Last_Login": "Último_Inicio_Sesión"
})

# Configuración de la página
st.set_page_config(page_title="Netflix Users Data", page_icon="📊", layout="wide")

# Imagen inicial
st.image('Netflix.jpg', caption='Netflix Users Data', use_container_width=True)

# Título y descripción
st.title('Análisis de Datos de Usuarios de Netflix')
st.subheader('Explora los insights de los usuarios de Netflix')

# Mostrar los datos

if st.checkbox("Mostrar todos los datos"):
    st.subheader("Vista completa de los datos")
    st.dataframe(df)
else:
    st.info("Haz clic en la casilla para mostrar los datos completos.")



# Análisis 1: Edad promedio por país con filtro múltiple
st.subheader("Edad Promedio por País")

# Selector de países (multiselección)
paises_disponibles = df['País'].unique()
paises_seleccionados = st.multiselect(
    "Selecciona los países que deseas analizar:",
    options=paises_disponibles,
    default=paises_disponibles  # Por defecto selecciona todos
)

# Filtrar el DataFrame según los países seleccionados
df_filtrado_paises = df[df['País'].isin(paises_seleccionados)]

# Calcular edad promedio por país
edad_promedio_por_pais = df_filtrado_paises.groupby('País')['Edad'].mean().sort_values(ascending=False)

# Gráfica
fig1 = px.bar(
    edad_promedio_por_pais,
    x=edad_promedio_por_pais.index,
    y=edad_promedio_por_pais.values,
    labels={'x': 'País', 'y': 'Edad Promedio'},
    title="Edad Promedio de Usuarios por País"
)
st.plotly_chart(fig1, use_container_width=True)

# Análisis 2: Correlación entre edad y horas vistas
if 'Horas_Vistas' in df.columns:
    correlacion = df[['Edad', 'Horas_Vistas']].corr().iloc[0, 1]
    st.write(f"La correlación entre edad y horas vistas es: {correlacion:.2f}")
    fig2 = px.scatter(df, x='Edad', y='Horas_Vistas', color='País',
                      title="Relación entre Edad y Horas Vistas")
    st.plotly_chart(fig2)

# Análisis 3: Usuarios por tipo de suscripción

st.subheader("Distribución por Tipo de Suscripción")

# Filtros interactivos
paises_disponibles = df['País'].unique()
paises_filtro = st.multiselect(
    "Filtrar por país:",
    options=paises_disponibles,
    default=paises_disponibles
)

edad_min, edad_max = int(df['Edad'].min()), int(df['Edad'].max())
edad_filtro = st.slider("Filtrar por rango de edad:", min_value=edad_min, max_value=edad_max, value=(edad_min, edad_max))

# Aplicar filtros
df_filtrado = df[
    (df['País'].isin(paises_filtro)) &
    (df['Edad'] >= edad_filtro[0]) &
    (df['Edad'] <= edad_filtro[1])
]

# Contar usuarios por tipo de suscripción
suscripciones = df_filtrado['Tipo_Suscripción'].value_counts()

# Gráfica
fig_suscripciones = px.pie(
    names=suscripciones.index,
    values=suscripciones.values,
    title="Distribución de Tipos de Suscripción (Filtrada)"
)
st.plotly_chart(fig_suscripciones, use_container_width=True)

# Análisis 4: Usuarios por país (Top 5)
st.subheader("Cantidad de Usuarios por País")

# Filtro para seleccionar cuántos países mostrar
num_paises = st.slider(
    "Selecciona cuántos países quieres mostrar",
    min_value=1,
    max_value=len(df['País'].value_counts()),
    value=10
)

# Contar usuarios por país, ordenar y limitar a los seleccionados
usuarios_por_pais = df['País'].value_counts().sort_values(ascending=False).head(num_paises)

# Gráfico interactivo con Plotly
fig4 = px.bar(
    usuarios_por_pais,
    x=usuarios_por_pais.index,
    y=usuarios_por_pais.values,
    labels={'x': 'País', 'y': 'Usuarios'},
    title=f"Top {num_paises} Países con Más Usuarios"
)

fig4.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig4, use_container_width=True)



#Edades con más usuarios (Top N edades)

st.subheader("Top Edades con Más Usuarios")

top_n = st.slider("Selecciona cuántas edades mostrar", 5, 20, 10)

edades_mas_comunes = df["Edad"].value_counts().sort_values(ascending=False).head(top_n)

fig_top_edades = px.bar(
    edades_mas_comunes,
    x=edades_mas_comunes.index,
    y=edades_mas_comunes.values,
    labels={"x": "Edad", "y": "Cantidad de Usuarios"},
    title=f"Top {top_n} Edades con Más Usuarios"
)

st.plotly_chart(fig_top_edades, use_container_width=True)

#Relación entre edad y horas vistas

st.subheader("Relación entre Edad y Horas Vistas")

fig_dispersion = px.scatter(
    df,
    x="Edad",
    y="Horas_Vistas",
    trendline="ols",
    color="País",
    title="Edad vs. Horas de Visualización"
)

st.plotly_chart(fig_dispersion, use_container_width=True)

#Género favorito

st.subheader("🎬 Análisis del Género Favorito de los Usuarios")

# Obtener los valores únicos de país
paises_unicos = df['País'].unique()

# Filtros interactivos
paises_seleccionados = st.multiselect("Selecciona país(es)", options=paises_unicos, default=paises_unicos)
rango_edad = st.slider("Selecciona el rango de edad", min_value=int(df['Edad'].min()), max_value=int(df['Edad'].max()), value=(18, 60))

# Filtrar el DataFrame según filtros
df_genero = df[
    (df['País'].isin(paises_seleccionados)) &
    (df['Edad'] >= rango_edad[0]) &
    (df['Edad'] <= rango_edad[1])
]

# Contar géneros favoritos
conteo_generos = df_genero['Género_Favorito'].value_counts().sort_values(ascending=True)

# Gráfico de barras horizontales
fig_genero = px.bar(
    x=conteo_generos.values,
    y=conteo_generos.index,
    orientation='h',
    labels={'x': 'Cantidad de Usuarios', 'y': 'Género Favorito'},
    title="Preferencias de Géneros por Edad y País"
)

st.plotly_chart(fig_genero, use_container_width=True)

