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


st.set_page_config(page_title="Resultados departamentos en Mérida", page_icon=":house:")
df = database.load_depas()
df['colloc'] = df['colloc'].str.title()

st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 35px; text-align: center'>Portales inmobiliarios y oferta de departamentos en Mérida</p>", unsafe_allow_html=True)

st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Algunos datos generales</p>", unsafe_allow_html=True)
#Length of the dataframe
st.markdown("<p style='font-family: Century Gothic;font-size: 15px; text-align: justified'>La base de datos cuenta con un total de <b>{:,}</b> registros de departamentos en venta en el municipio de Mérida, Yucatán.</p>".format(df.shape[0]), unsafe_allow_html=True)

st.markdown("---")

##############
#####Mapa#####
###############
df_mapa=df.dropna(subset=['lat','lon'])


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


def get_color(feature):
    gm_value = feature['properties']['gm_2020']
    return color_mapping.get(gm_value, '#FFFFFF')

st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Concentración territorial de la oferta</p>", unsafe_allow_html=True)
st.markdown("<p style='font-family: Century Gothic;font-size: 15px; text-align: justified'>Del total de registros, el <b>{:.1f}%</b> cuenta con coordenadas para poder identificar su ubicación en el mapa.</p>".format(df_mapa.shape[0]/df.shape[0]*100,df_mapa.shape[0]/df.shape[0]*100), unsafe_allow_html=True)

import folium
import branca.colormap as cm

df=database.load_terrenos()
colonias=database.load_colonias()
df=df.dropna(subset=['lat','lon'])
df=gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df["lon"],df["lat"]))
df.crs=colonias.crs
combinada=gpd.sjoin(colonias,df,how='inner',op='contains')
combinada=combinada.groupby(['geometry']).size().reset_index(name='terrenos_venta')
colonias=colonias.merge(combinada,how='left',on='geometry')



m = folium.Map(location=[20.983953, -89.6463737], zoom_start=11)

# Adding Google Satellite tile layer
google_satellite = folium.TileLayer(
    tiles='https://www.google.com/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}',
    attr='Google',
    name='Google Satellite',
    overlay=False,
    control=True
)
google_satellite.add_to(m)

# Adding CartoDB Positron tile layer
cartodb_positron = folium.TileLayer(
    tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
    attr='CartoDB',
    name='CartoDB Positron',
    overlay=False,
    control=True
).add_to(m)

#
# m = folium.Map(location=[20.983953,-89.6463737], zoom_start=11,tiles="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}", attr="Elaboración propia con información de portales inmobiliarios")

#División por colonias
colonia_marker=folium.FeatureGroup(name="Colonias",show=True)
#Agregar capa de colonias
folium.GeoJson(
    colonias,
    style_function=lambda feature: {
        #Rellenar por grado de marginación
        'fillColor': 'transparent',

        'fillOpacity': 0.4,
        'color': '#000000',   # You can adjust the border color if needed
        'weight': 1,
        'dashArray': '5, 5'  # Dashed borders, remove this if not desired
    },


tooltip = folium.GeoJsonTooltip(
    fields=["colonia", "terrenos_venta"],
    aliases=["Colonia: ", "Terrenos en venta: "]
).add_to(colonia_marker)

).add_to(m)



agg_data = df_mapa.groupby(['lat', 'lon']).size().reset_index(name='counts')

# Finding vmin and vmax for the heatmap
vmin_value = agg_data['counts'].min()
vmax_value = agg_data['counts'].max()

# Creating the heatmap
HeatMap(data=agg_data[['lat', 'lon', 'counts']], radius=8, max_zoom=14,name="Terrenos",overlay=True, control=True,show=True,

        gradient={0.0: 'yellow', 0.5: 'orange', 1.0: 'red'}).add_to(m)

cmap = branca.colormap.LinearColormap(
    #colors=['green', 'cyan', 'blue'],
    colors=['yellow', 'orange', 'red'],
    index=[vmin_value, (vmin_value + vmax_value) / 2, vmax_value],
    vmin=vmin_value, vmax=vmax_value,
    caption="Departamentos"
)

# Adding the colormap to the map
m.add_child(cmap)


folium.LayerControl().add_to(m)

# Display the map in Streamlit
folium_static(m)
