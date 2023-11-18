import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df=pd.read_csv("https://raw.githubusercontent.com/claudiodanielpc/vivi_yuca_result/main/data/viviyuca.csv")
    return df