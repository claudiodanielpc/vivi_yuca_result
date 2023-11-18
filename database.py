import pandas as pd
from sqlalchemy import create_engine
import streamlit as st





@st.cache_data
def load_data():
    username = 'postgres'
    password = 'olivia14'

    # Setting up the connection string for SQLAlchemy
    engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/postgres')

    # Replace 'table_name' with the actual name of your table
    table_name = 'vivienda_yucatan'

    # Invoke the table into a pandas DataFrame
    df = pd.read_sql_table(table_name, engine)
    return df