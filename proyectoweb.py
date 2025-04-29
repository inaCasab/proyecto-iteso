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
st.image('Netflix.png', caption='Netflix Users Data', use_container_width=True)

# Título y descripción
st.title('Análisis de Datos de Usuarios de Netflix')
st.subheader('Explora los insights de los usuarios de Netflix')

#Nombres
st.markdown("### Creado por Ina Gabriela Casab Covarrubias y Leonardo Gamboa Cruz")

# Mostrar los datos

# Inicializar el estado si no existe
if 'mostrar_datos' not in st.session_state:
    st.session_state.mostrar_datos = False

# Cambiar el texto del botón 
boton_texto = "Ocultar datos" if st.session_state.mostrar_datos else "Mostrar todos los datos"

#Alternar el estado
if st.button(boton_texto):
    st.session_state.mostrar_datos = not st.session_state.mostrar_datos

# Mostrar u ocultar los datos
if st.session_state.mostrar_datos:
    st.subheader("Vista completa de los datos")
    st.dataframe(df)
else:
    st.info("Haz clic en el botón para mostrar los datos completos.")



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





# Análisis 2: 

st.subheader("Relación entre Edad y Horas Vistas")

# Filtros interactivos 
paises_unicos = df['País'].unique()

paises_seleccionados = st.multiselect(
    "Selecciona país(es)", 
    options=paises_unicos, 
    default=paises_unicos
)

rango_edad = st.slider(
    "Selecciona el rango de edad",
    min_value=int(df['Edad'].min()),
    max_value=int(df['Edad'].max()),
    value=(18, 60)
)

# Aplicar los filtros
df_filtrado = df[
    (df['País'].isin(paises_seleccionados)) &
    (df['Edad'] >= rango_edad[0]) & 
    (df['Edad'] <= rango_edad[1])
]

# Seleccionar columnas numéricas
df_numerico = df_filtrado[['Edad', 'Horas_Vistas']].dropna()

# matriz de correlación
matriz_corr = df_numerico.corr()

# Graficar 
fig_corr = px.imshow(
    matriz_corr,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    zmin=-1,
    zmax=1,
    title="Matriz de Correlación entre Edad y Horas Vistas"
)

st.plotly_chart(fig_corr, use_container_width=True)





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
    title="Distribución de Tipos de Suscripción"
)
st.plotly_chart(fig_suscripciones, use_container_width=True)


#Análisis 3.1: horas vistas por tipo de suscripción

horas_promedio_suscripcion = df.groupby('Tipo_Suscripción')['Horas_Vistas'].mean().reset_index()

# Mostrar el análisis
st.write("### Horas Promedio Vistas por Tipo de Suscripción")
st.write(horas_promedio_suscripcion)

# Crear la gráfica interactiva con Plotly
fig = px.bar(horas_promedio_suscripcion, 
             x='Tipo_Suscripción', 
             y='Horas_Vistas', 
             title='Horas Promedio Vistas por Tipo de Suscripción',
             labels={'Horas_Vistas': 'Horas Promedio Vistas', 'Tipo_Suscripción': 'Tipo de Suscripción'},
             text='Horas_Vistas')  # Mostrar el valor de las barras al pasar el mouse

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig)




# Análisis 4: Usuarios por país 
st.subheader("Cantidad de Usuarios por País")

# Filtro para países 
num_paises = st.slider(
    "Selecciona cuántos países quieres mostrar",
    min_value=1,
    max_value=len(df['País'].value_counts()),
    value=10
)

# Contar y ordenar usuarios por país
usuarios_por_pais = df['País'].value_counts().sort_values(ascending=False).head(num_paises)

# Gráficar
fig4 = px.bar(
    usuarios_por_pais,
    x=usuarios_por_pais.index,
    y=usuarios_por_pais.values,
    labels={'x': 'País', 'y': 'Usuarios'},
    title=f"Top {num_paises} Países con Más Usuarios"
)

fig4.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig4, use_container_width=True)



#Edades con más usuarios 

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








#Análisis
#Género favorito

st.subheader("Análisis del Género Favorito de los Usuarios")

# Filtros propios
paises_genero = df['País'].unique()
paises_genero_seleccionados = st.multiselect("Selecciona país(es) para género favorito", options=paises_genero, default=paises_genero)
rango_edad_genero = st.slider(
    "Selecciona el rango de edad para género favorito",
    min_value=int(df['Edad'].min()),
    max_value=int(df['Edad'].max()),
    value=(18, 60)
)

# Filtrar los datos
df_genero = df[
    (df['País'].isin(paises_genero_seleccionados)) &
    (df['Edad'] >= rango_edad_genero[0]) &
    (df['Edad'] <= rango_edad_genero[1])
]

conteo_generos = df_genero['Género_Favorito'].value_counts().sort_values(ascending=True)

fig_genero = px.bar(
    x=conteo_generos.values,
    y=conteo_generos.index,
    orientation='h',
    labels={'x': 'Cantidad de Usuarios', 'y': 'Género Favorito'},
    title="Preferencias de Géneros por Edad y País"
)

st.plotly_chart(fig_genero, use_container_width=True)

#------------------------------------------


# Filtros interactivos
paises_seleccionados = st.multiselect("Selecciona país(es)", options=paises_unicos, default=paises_unicos)
rango_edad = st.slider("Selecciona el rango de edad", min_value=int(df['Edad'].min()), max_value=int(df['Edad'].max()), value=(18, 60)).  

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



