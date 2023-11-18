import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit.elements import spinner
from IPython.display import IFrame
import database

# username = 'postgres'
# password = 'olivia14'

# # Setting up the connection string for SQLAlchemy
# engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/postgres')

# # Replace 'table_name' with the actual name of your table
# table_name = 'vivienda_yucatan'

# # Invoke the table into a pandas DataFrame
# df = pd.read_sql_table(table_name, engine)


st.set_page_config(page_title="Resultados vivienda en Mérida", page_icon=":house:")
df = database.load_data()

st.markdown("<p style='font-family: Montserrat; font-weight: bold;font-size: 35px; text-align: center'>Portales inmobiliarios y oferta disponible de vivienda nueva en Mérida</p>", unsafe_allow_html=True)

# #Histograma de precios utilizando plotly express
# st.markdown("<p style='font-family: Montserrat; font-weight: bold;font-size: 25px; text-align: center'>Histograma de precios</p>", unsafe_allow_html=True)
# fig = px.histogram(df, x='precio', nbins=10, title='Histograma de precios')
# fig.show()

