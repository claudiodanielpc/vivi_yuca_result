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


#Gráfica de barras	
st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>¿En qué colonias o localidades se concentra la oferta?</p>", unsafe_allow_html=True)
fig = px.bar(df.sort_values(by='count',ascending=False).head(10), x='count', y='localidad', orientation='h',color='localidad',color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(showlegend=False)
st.plotly_chart(fig)







st.markdown("---")

