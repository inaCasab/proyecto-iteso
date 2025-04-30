import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

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

# Obtener lista única de países
paises_unicos = df['País'].unique()

# Filtro 
paises_seleccionados = st.multiselect(
    "Selecciona país(es)",
    options=paises_unicos,
    default=paises_unicos,
    key="filtro_paises"
)

rango_edad = st.slider(
    "Selecciona el rango de edad",
    min_value=int(df['Edad'].min()),
    max_value=int(df['Edad'].max()),
    value=(18, 60),
    key="filtro_rango_edad"
)

# Filtrar el DataFrame
df_filtrado = df[
    (df['País'].isin(paises_seleccionados)) &
    (df['Edad'] >= rango_edad[0]) & (df['Edad'] <= rango_edad[1])
]

# Agrupar por país y edad promedio, sacando promedio de horas vistas
df_agrupado = df_filtrado.groupby(['País', 'Edad'], as_index=False)['Horas_Vistas'].mean()

# Gráfico de líneas
st.subheader("Relación entre Edad y Horas Vistas (promedio por edad)")

fig_linea = px.line(
    df_agrupado,
    x="Edad",
    y="Horas_Vistas",
    color="País",
    title="Edad vs. Horas de Visualización (Promedios)"
)

st.plotly_chart(fig_linea, use_container_width=True)




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


# Análisis: Matriz de correlación género favorito y país

st.subheader("Correlación entre el Género Favorito y elrango_edad_calor = st.slider(
    "Selecciona el rango de edad:",
    min_value=int(df['Edad'].min()),
    max_value=int(df['Edad'].max()),
    value=(int(df['Edad'].min()), int(df['Edad'].max())),
    key="matriz_calor_edad"
)

# Filtrar el DataFrame según los filtros seleccionados
df_calor = df[
    (df['País'].isin(paises_seleccionados_calor)) &
    (df['Edad'] >= rango_edad_calor[0]) &
    (df['Edad'] <= rango_edad_calor[1])
]

# Crear la tabla cruzada
genero_por_pais = df_calor.groupby(['País', 'Género_Favorito']).size().unstack(fill_value=0)

# Crear el heatmap con Plotly
fig_heatmap = go.Figure(data=go.Heatmap(
    z=genero_por_pais.values,
    x=genero_por_pais.columns,
    y=genero_por_pais.index,
    colorscale='YlGnBu',
    hoverongaps=False,
    showscale=True
))

fig_heatmap.update_layout(
    title="Preferencia de Géneros por País y Edad",
    xaxis_title="Género Favorito",
    yaxis_title="País"
)

# Mostrar en Streamlit
st.plotly_chart(fig_heatmap, use_container_width=True) País")

# Filtros interactivos
paises_calor = df['País'].unique()
paises_seleccionados_calor = st.multiselect(
    "Selecciona los países para visualizar:",
    options=sorted(paises_calor),
    default=list(paises_calor),
    key="matriz_calor_paises"
)


# Análisis: Matriz de correlación género favorito y edad
st.subheader("Matriz de Calor: Género Favorito por Edad")

# Filtros interactivos
paises_matriz_edad = df['País'].unique()
paises_seleccionados_matriz_edad = st.multiselect(
    "Selecciona los países para visualizar:",
    options=sorted(paises_matriz_edad),
    default=list(paises_matriz_edad),
    key="matriz_calor_por_edad_paises"
)

rango_edad_matriz = st.slider(
    "Selecciona el rango de edad:",
    min_value=int(df['Edad'].min()),
    max_value=int(df['Edad'].max()),
    value=(int(df['Edad'].min()), int(df['Edad'].max())),
    key="matriz_calor_por_edad_rango"
)

# Filtrar el DataFrame
df_matriz_edad = df[
    (df['País




