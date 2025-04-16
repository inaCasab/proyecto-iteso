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

    
# Filtros interactivos en la barra lateral
st.sidebar.header("Filtros")
pais_seleccionado = st.sidebar.selectbox('Selecciona un país', df['País'].unique())
edad_minima = st.sidebar.slider('Edad mínima', min_value=int(df['Edad'].min()), max_value=int(df['Edad'].max()), value=20)

# Filtrar los datos
df_filtrado = df[(df['País'] == pais_seleccionado) & (df['Edad'] >= edad_minima)]

# Mostrar resultados filtrados
st.write(f"Datos filtrados por país: {pais_seleccionado} y edad mayor o igual a {edad_minima}")
st.dataframe(df_filtrado)

# Revisar valores nulos
null_counts = df.isnull().sum()
total_nulls = null_counts.sum()
st.write(f"Total de celdas con valores nulos: {total_nulls}")

# Análisis 1: Edad promedio por país
edad_promedio_por_pais = df.groupby('País')['Edad'].mean().sort_values(ascending=False)
fig1 = px.bar(edad_promedio_por_pais, x=edad_promedio_por_pais.index, y=edad_promedio_por_pais.values,
              labels={'x': 'País', 'y': 'Edad Promedio'}, title="Edad Promedio de Usuarios por País")
st.plotly_chart(fig1)

# Análisis 2: Correlación entre edad y horas vistas
if 'Horas_Vistas' in df.columns:
    correlacion = df[['Edad', 'Horas_Vistas']].corr().iloc[0, 1]
    st.write(f"La correlación entre edad y horas vistas es: {correlacion:.2f}")
    fig2 = px.scatter(df, x='Edad', y='Horas_Vistas', color='País',
                      title="Relación entre Edad y Horas Vistas")
    st.plotly_chart(fig2)

# Análisis 3: Usuarios por tipo de suscripción
suscripciones = df['Tipo_Suscripción'].value_counts()
fig3 = px.pie(suscripciones, names=suscripciones.index, values=suscripciones.values,
              title="Distribución por Tipo de Suscripción")
st.plotly_chart(fig3)

# Análisis 4: Usuarios por país (Top 5)
top_paises = df['País'].value_counts().head(5)
fig4 = px.bar(top_paises, x=top_paises.index, y=top_paises.values,
              labels={'x': 'País', 'y': 'Usuarios'}, title="Top 5 Países con más Usuarios")
st.plotly_chart(fig4)

# Análisis 5: Países con menor cantidad de usuarios (Bottom 5)
bottom_paises = df['País'].value_counts().tail(5)
fig5 = px.bar(bottom_paises, x=bottom_paises.index, y=bottom_paises.values,
              labels={'x': 'País', 'y': 'Usuarios'}, title="Países con Menos Usuarios")
st.plotly_chart(fig5)

# Análisis 6: Rango de horas vistas
bins = [0, 5, 10, 15, 20, 25, 30, 50]
labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '30+']
df['Rango_Horas'] = pd.cut(df['Horas_Vistas'], bins=bins, labels=labels, right=False)
tabla_horas = df['Rango_Horas'].value_counts().sort_in






