import pandas as pd
import streamlit as st
import geopandas as gpd

@st.cache_data
def load_data():
    df=pd.read_csv("https://raw.githubusercontent.com/claudiodanielpc/vivi_yuca_result/main/data/viviyuca.csv")
    return df

@st.cache_data
def load_colonias():
    df = gpd.read_file("https://github.com/claudiodanielpc/yucascraper/raw/main/yucascraper/catalogos/yucatan_colonias.shp")
    return df
