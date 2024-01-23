import pandas as pd
import streamlit as st
import geopandas as gpd

@st.cache_data
def load_data():
    df=pd.read_csv("https://raw.githubusercontent.com/claudiodanielpc/vivi_yuca_result/main/data/viviyuca_limpia.csv")
    return df

@st.cache_data
def load_colonias():
    df = gpd.read_file("https://raw.githubusercontent.com/claudiodanielpc/vivi_yuca_result/main/data/colonias/merida_colonias.geojson")
    return df
@st.cache_data
def load_terrenos():
    df = pd.read_csv("https://raw.githubusercontent.com/claudiodanielpc/vivi_yuca_result/main/data/terrenosyuca_limpia.csv")
    return df


@st.cache_data
def load_depas():
    df = pd.read_csv("https://raw.githubusercontent.com/claudiodanielpc/vivi_yuca_result/main/data/depasyuca_limpia.csv")
    return df

