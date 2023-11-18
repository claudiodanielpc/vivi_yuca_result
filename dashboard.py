import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit.elements import spinner
from IPython.display import IFrame
import database
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static




st.set_page_config(page_title="Resultados vivienda en Mérida", page_icon=":house:")
df = database.load_data()
df['colloc'] = df['colloc'].str.title()


st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 35px; text-align: center'>Portales inmobiliarios y oferta de vivienda nueva en Mérida</p>", unsafe_allow_html=True)



st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Algunos datos generales</p>", unsafe_allow_html=True)
#Length of the dataframe
st.markdown("<p style='font-family: Century Gothic;font-size: 15px; text-align: justified'>La base de datos cuenta con un total de <b>{:,}</b> registros de vivienda nueva en venta en el municipio de Mérida, Yucatán.</p>".format(df.shape[0]), unsafe_allow_html=True)

st.markdown("---")

#Mapa
df_mapa=df.dropna(subset=['lat','lon'])


st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Concentración territorial de la oferta</p>", unsafe_allow_html=True)
st.markdown("<p style='font-family: Century Gothic;font-size: 15px; text-align: justified'>Del total de registros, el <b>{:.1f}%</b> cuenta con coordenadas para poder identificar su ubicación en el mapa.</p>".format(df_mapa.shape[0]/df.shape[0]*100,df_mapa.shape[0]/df.shape[0]*100), unsafe_allow_html=True)
m = folium.Map(location=[21.0000, -89.5000], zoom_start=10,tiles="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}", attr="Google Satellite")
HeatMap(data=df_mapa[['lat', 'lon']], radius=8, max_zoom=13).add_to(m)
folium_static(m)

##Añadir sidebar
st.sidebar.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Fuente de datos</p>", unsafe_allow_html=True)
st.sidebar.write("<p style='font-family: Montserrat;'>Para el presente proyecto, se descargó información de los siguientes portales:</p>", unsafe_allow_html=True)
#Lamudi
st.sidebar.markdown(
f"<div style='text-align:center;font-family:montserrat;'>"
f"<img src='https://www.lamudi.com.mx/journal/wp-content//uploads/2020/02/lamudi-9-marzo.png' alt='Lamudi' width='70'/>"
#Añadir url para redirigir a la página del INEGI
f"<p><a href='https://www.lamudi.com.mx/'>Lamudi</a></p>"
f"</div>",
unsafe_allow_html=True)

st.sidebar.write(" ")

#Goodlers
st.sidebar.markdown(
f"<div style='text-align:center;font-family:montserrat;'>"
f"<img src='https://goodlers.com/_nuxt/img/fb7d937.png' alt='Goodlers' width='70'/>"
#Añadir url para redirigir a la página del INEGI
f"<p><a href='https://goodlers.com/'>Goodlers</a></p>"
f"</div>",
unsafe_allow_html=True)

st.sidebar.write(" ")

#Easybroker
st.sidebar.markdown(
f"<div style='text-align:center;font-family:montserrat;'>"
f"<img src='https://www.easybroker.com/brand_files/logo.png' alt='Easybroker' width='70'/>"
#Añadir url para redirigir a la página del INEGI
f"<p><a href='https://www.easybroker.com/mx/'>Easybroker</a></p>"
f"</div>",
unsafe_allow_html=True)

st.sidebar.write(" ")

#Inmuebles24
st.sidebar.markdown(
f"<div style='text-align:center;font-family:montserrat;'>"
f"<img src='https://surveymonkey-assets.s3.amazonaws.com/survey/297849572/d1726151-bb64-4ee7-a3ab-429aaaf70a07.png' alt='Inmuebles24' width='70'/>"
#Añadir url para redirigir a la página del INEGI
f"<p><a href='https://www.inmuebles24.com/'>Inmuebles24</a></p>"
f"</div>",
unsafe_allow_html=True)





#Gráfica de registros por colonia
localidad_counts = df['colloc'].value_counts().reset_index()
localidad_counts.columns = ['colloc', 'count']
#Obtener porcentaje
localidad_counts['porcentaje'] = localidad_counts['count'] / localidad_counts['count'].sum() * 100
#Ordenar y dejar los 20 primeros
localidad_counts = localidad_counts.sort_values(by='porcentaje', ascending=False).head(20)
#Localidades con primera letra en mayúscula
localidad_counts['colloc'] = localidad_counts['colloc'].str.title()

# Display the header using Markdown
st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>¿En qué colonias o localidades se concentra la oferta?</p>", unsafe_allow_html=True)

# Create the bar chart with Plotly Express
fig = px.bar(localidad_counts.sort_values(by='porcentaje', ascending=True),

    x='porcentaje',
    y='colloc',
    orientation='h',
    color='porcentaje',
    color_continuous_scale='YlOrRd',
)
fig.update_layout(
    coloraxis_colorbar=dict(
        title="%",
        
        dtick=3
    ))

# Update the layout of the figure
fig.update_layout(
    showlegend=False,
    yaxis_title=None,  # Removes the y-axis title if desired
    xaxis_title="Porcentaje",  # Customize the x-axis title to represent frequency
 # Ensures the highest value is at the top
 annotations=[
        go.layout.Annotation(
            text='Fuente: Elaboración propia con datos de Goodlers, Inmuebles24, Lamudi y Easybroker',
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            showarrow=False,
            font=dict(
                family='Century Gothic',
                size=12,
                color='grey'
            )
        )
    ]
)

# Render the bar chart in Streamlit
st.plotly_chart(fig)



st.markdown("---")
st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>¿Cómo se distribuyen los precios por zona?</p>", unsafe_allow_html=True)


colloc=df.copy()
#Eliminar registros con colloc en nan
colloc=colloc.dropna(subset=['colloc'])

# Agregar una opción "Total" a las opciones de colloc
unique_colloc = list(colloc['colloc'].unique())
#Ordenar alfabéticamente
unique_colloc.sort()
unique_colloc = ['Total'] + unique_colloc
selected_colloc = st.selectbox('Selecciona una categoría', unique_colloc)

# Filtrar los datos basado en la selección
if selected_colloc == 'Total':
    filtered_df = colloc
else:
    filtered_df = colloc[colloc['colloc'] == selected_colloc]

# Crear el histograma
fig = px.histogram(filtered_df, x="precio", nbins=20, color_discrete_sequence=['#fca311'])
fig.update_layout(
    xaxis_title="Precio",
    yaxis_title="Frecuencia",
    annotations=[
        go.layout.Annotation(
            text='Fuente: Elaboración propia con datos de Goodlers, Inmuebles24, Lamudi y Easybroker',
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            showarrow=False,
            font=dict(
                family='Century Gothic',
                size=12,
                color='grey'
            )
        )
    ]
)

# Mostrar el histograma en la aplicación Streamlit
st.plotly_chart(fig)


st.markdown("---")  

csv = df.to_csv(index=False).encode('utf-8')

st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Descargar Base de Datos Completa</p>", unsafe_allow_html=True)

st.download_button(
    label="Descargar datos como CSV",
    data=csv,
    file_name='base_de_datos_completa.csv',
    mime='text/csv',
)

