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
