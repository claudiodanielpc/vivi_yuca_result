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
st.markdown("<p style='font-family: Century Gothic;font-size: 15px; text-align: justified'>El presente análisis se realizó con base en la información de los portales inmobiliarios de <a href='https://goodlers.com/' target='_blank'>Goodlers</a>, <a href='https://www.inmuebles24.com/' target='_blank'>Inmuebles24</a>, <a href='https://www.lamudi.com.mx/' target='_blank'>Lamudi</a> y <a href='https://www.easybroker.com/mx' target='_blank'>Easybroker</a>.</p>", unsafe_allow_html=True)
#Length of the dataframe
st.markdown("<p style='font-family: Century Gothic;font-size: 15px; text-align: justified'>La base de datos cuenta con un total de <b>{:,}</b> registros de vivienda nueva en venta.</p>".format(df.shape[0]), unsafe_allow_html=True)

st.markdown("---")

#Mapa
df_mapa=df.dropna(subset=['lat','lon'])


st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Concentración territorial de la oferta</p>", unsafe_allow_html=True)
st.markdown("<p style='font-family: Century Gothic;font-size: 15px; text-align: justified'>Del total de registros, el <b>{:.1f}%</b> cuenta con coordenadas para poder identificar su ubicación en el mapa.</p>".format(df_mapa.shape[0]/df.shape[0]*100,df_mapa.shape[0]/df.shape[0]*100), unsafe_allow_html=True)
m = folium.Map(location=[21.0000, -89.5000], zoom_start=10,tiles="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}", attr="Google Satellite")
HeatMap(data=df_mapa[['lat', 'lon']], radius=8, max_zoom=13).add_to(m)
folium_static(m)



#Gráfica por localidad
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


# Suponiendo que df es tu DataFrame con las columnas 'precio' y 'colloc'
# df = pd.DataFrame(...)

# Agregar una opción "Total" a las opciones de colloc
unique_colloc = ['Total'] + list(df['colloc'].unique())
selected_colloc = st.selectbox('Selecciona una categoría', unique_colloc)

# Filtrar los datos basado en la selección
if selected_colloc == 'Total':
    filtered_df = df
else:
    filtered_df = df[df['colloc'] == selected_colloc]

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


