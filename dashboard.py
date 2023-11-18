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

st.markdown("<p style='font-family: Montserrat; font-weight: bold;font-size: 35px; text-align: center'>Portales inmobiliarios y oferta disponible de vivienda nueva en Mérida</p>", unsafe_allow_html=True)



st.markdown("<p style='font-family: Montserrat; font-weight: bold;font-size: 20px; text-align: center'>¿Dónde se concentra el rezago habitacional?</p>", unsafe_allow_html=True)
st.markdown("<p style='font-family: Montserrat;font-size: 15px; text-align: justified'>El rezago habitacional se localiza principalmente en las entidades del sur, sureste de nuestro país: </p>", unsafe_allow_html=True)
df_mapa=df.dropna(subset=['lat','lon'])


st.markdown("<p style='font-family: Montserrat; font-weight: bold;font-size: 20px; text-align: center'>Concentración territorial de la oferta</p>", unsafe_allow_html=True)
m = folium.Map(location=[21.0000, -89.5000], zoom_start=10,tiles="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}", attr="Google Satellite")
HeatMap(data=df_mapa[['lat', 'lon']], radius=8, max_zoom=13).add_to(m)
folium_static(m)

