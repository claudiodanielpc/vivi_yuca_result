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
import branca
import branca.colormap as cm
import geopandas as gpd


st.set_page_config(page_title="Resultados terrenos en Mérida", page_icon=":house:")


st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 35px; text-align: center'>Portales inmobiliarios y oferta de terrenos en Mérida</p>", unsafe_allow_html=True)


# Separator
st.sidebar.markdown("---")

# Sidebar - Custom Markdown for data source title
st.sidebar.markdown(
    "<p style='font-family: Century Gothic; font-weight: bold; font-size: 20px; text-align: center'>Fuente de datos</p>",
    unsafe_allow_html=True)

# Sidebar - Custom Markdown for data source description
st.sidebar.markdown(
    "<p style='font-family: Century Gothic;'>Para el presente proyecto, se descargó información de los siguientes portales:</p>",
    unsafe_allow_html=True)

# Sidebar - Lamudi
st.sidebar.markdown(
    f"<div style='text-align:center;font-family:montserrat;'>"
    f"<img src='https://www.lamudi.com.mx/journal/wp-content//uploads/2020/02/lamudi-9-marzo.png' alt='Lamudi' width='70'/>"
    f"<p><a href='https://www.lamudi.com.mx/'>Lamudi</a></p>"
    f"</div>",
    unsafe_allow_html=True)

# Sidebar - Goodlers
st.sidebar.markdown(
    f"<div style='text-align:center;font-family:montserrat;'>"
    f"<img src='https://goodlers.com/_nuxt/img/fb7d937.png' alt='Goodlers' width='70'/>"
    f"<p><a href='https://goodlers.com/'>Goodlers</a></p>"
    f"</div>",
    unsafe_allow_html=True)

# Sidebar - Easybroker
st.sidebar.markdown(
    f"<div style='text-align:center;font-family:montserrat;'>"
    f"<img src='https://www.easybroker.com/brand_files/logo.png' alt='Easybroker' width='70'/>"
    f"<p><a href='https://www.easybroker.com/mx/'>Easybroker</a></p>"
    f"</div>",
    unsafe_allow_html=True)

# Sidebar - Inmuebles24
st.sidebar.markdown(
    f"<div style='text-align:center;font-family:montserrat;'>"
    f"<img src='https://surveymonkey-assets.s3.amazonaws.com/survey/297849572/d1726151-bb64-4ee7-a3ab-429aaaf70a07.png' alt='Inmuebles24' width='70'/>"
    f"<p><a href='https://www.inmuebles24.com/'>Inmuebles24</a></p>"
    f"</div>",
    unsafe_allow_html=True)