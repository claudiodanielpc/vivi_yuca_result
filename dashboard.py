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




st.set_page_config(page_title="Resultados vivienda en Mérida", page_icon=":house:")
df = database.load_data()
df['colloc'] = df['colloc'].str.title()


st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 35px; text-align: center'>Portales inmobiliarios y oferta para adquisición de vivienda en Mérida</p>", unsafe_allow_html=True)



st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Algunos datos generales</p>", unsafe_allow_html=True)
#Length of the dataframe
st.markdown("<p style='font-family: Century Gothic;font-size: 15px; text-align: justified'>La base de datos cuenta con un total de <b>{:,}</b> registros de vivienda en venta en el municipio de Mérida, Yucatán.</p>".format(df.shape[0]), unsafe_allow_html=True)

st.markdown("---")

##############
#####Mapa#####
###############
df_mapa=df.dropna(subset=['lat','lon'])

color_mapping = {
    "Muy bajo": "#ffffb2",  # lightest yellow in YlOrRd scheme
    "Bajo": "#fecc5c",     # light orange
    "Medio": "#fd8d3c",    # orange
    "Alto": "#f03b20",     # dark orange/red
    "Muy alto": "#bd0026"  # darkest red in YlOrRd scheme
    }


def get_color(feature):
    gm_value = feature['properties']['gm_2020']
    return color_mapping.get(gm_value, '#FFFFFF')

st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Concentración territorial de la oferta</p>", unsafe_allow_html=True)
st.markdown("<p style='font-family: Century Gothic;font-size: 15px; text-align: justified'>Del total de registros, el <b>{:.1f}%</b> cuenta con coordenadas para poder identificar su ubicación en el mapa.</p>".format(df_mapa.shape[0]/df.shape[0]*100,df_mapa.shape[0]/df.shape[0]*100), unsafe_allow_html=True)


import folium
import branca.colormap as cm

# Your existing map centered around the specified location
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
)
cartodb_positron.add_to(m)


#
# m = folium.Map(location=[20.983953, -89.6463737], zoom_start=11,tiles="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}", attr="Elaboración propia con información de portales inmobiliarios")

#División por colonias
colonia_marker=folium.FeatureGroup(name="Colonias",show=True)
#Agregar capa de colonias
folium.GeoJson(
    database.load_colonias(),
    style_function=lambda feature: {
        #Rellenar por grado de marginación
        'fillColor': 'transparent',

        'fillOpacity': 0.4,
        'color': '#000000',   # You can adjust the border color if needed
        'weight': 1,
        'dashArray': '5, 5'  # Dashed borders, remove this if not desired
    },
tooltip=folium.GeoJsonTooltip(fields=["colonia"],aliases=["Colonia: "])).add_to(colonia_marker
                                                                                                    )
colonia_marker.add_to(m)


agg_data = df_mapa.groupby(['lat', 'lon']).size().reset_index(name='counts')

# Finding vmin and vmax for the heatmap
vmin_value = agg_data['counts'].min()
vmax_value = agg_data['counts'].max()

# Creating the heatmap
HeatMap(data=agg_data[['lat', 'lon', 'counts']], radius=8, max_zoom=14,name="Viviendas",overlay=True, control=True,show=True).add_to(m)

cmap = branca.colormap.LinearColormap(
    colors=['green', 'cyan', 'blue'],
    index=[vmin_value, (vmin_value + vmax_value) / 2, vmax_value],
    vmin=vmin_value, vmax=vmax_value,
    caption="Viviendas"
)

# Adding the colormap to the map
m.add_child(cmap)


folium.LayerControl().add_to(m)

# Display the map in Streamlit
folium_static(m) 


# ##Añadir sidebar
# st.sidebar.selectbox('Selecciona la página que deseas ver', ['Viviendas', 'Terrenos'])
# st.sidebarmarkdown("---")
#
# st.sidebar.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Fuente de datos</p>", unsafe_allow_html=True)
# st.sidebar.write("<p style='font-family: Century Gothic;'>Para el presente proyecto, se descargó información de los siguientes portales:</p>", unsafe_allow_html=True)
# #Lamudi
# st.sidebar.markdown(
# f"<div style='text-align:center;font-family:montserrat;'>"
# f"<img src='https://www.lamudi.com.mx/journal/wp-content//uploads/2020/02/lamudi-9-marzo.png' alt='Lamudi' width='70'/>"
# #Añadir url para redirigir a la página del INEGI
# f"<p><a href='https://www.lamudi.com.mx/'>Lamudi</a></p>"
# f"</div>",
# unsafe_allow_html=True)
#
# st.sidebar.write(" ")
#
# #Goodlers
# st.sidebar.markdown(
# f"<div style='text-align:center;font-family:montserrat;'>"
# f"<img src='https://goodlers.com/_nuxt/img/fb7d937.png' alt='Goodlers' width='70'/>"
# #Añadir url para redirigir a la página del INEGI
# f"<p><a href='https://goodlers.com/'>Goodlers</a></p>"
# f"</div>",
# unsafe_allow_html=True)
#
# st.sidebar.write(" ")
#
# #Easybroker
# st.sidebar.markdown(
# f"<div style='text-align:center;font-family:montserrat;'>"
# f"<img src='https://www.easybroker.com/brand_files/logo.png' alt='Easybroker' width='70'/>"
# #Añadir url para redirigir a la página del INEGI
# f"<p><a href='https://www.easybroker.com/mx/'>Easybroker</a></p>"
# f"</div>",
# unsafe_allow_html=True)
#
# st.sidebar.write(" ")
#
# #Inmuebles24
# st.sidebar.markdown(
# f"<div style='text-align:center;font-family:montserrat;'>"
# f"<img src='https://surveymonkey-assets.s3.amazonaws.com/survey/297849572/d1726151-bb64-4ee7-a3ab-429aaaf70a07.png' alt='Inmuebles24' width='70'/>"
# #Añadir url para redirigir a la página del INEGI
# f"<p><a href='https://www.inmuebles24.com/'>Inmuebles24</a></p>"
# f"</div>",
# unsafe_allow_html=True)

# Sidebar - Selectbox for page selection
#st.sidebar.selectbox('Selecciona la página que deseas ver', ['Viviendas', 'Terrenos'])

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





#Gráfica de registros por colonia
localidad_counts = df['colloc'].value_counts().reset_index()
localidad_counts.columns = ['colloc', 'count']
#Obtener porcentaje
localidad_counts['porcentaje'] = localidad_counts['count'] / localidad_counts['count'].sum() * 100
#Ordenar y dejar los 20 primeros
localidad_counts = localidad_counts.sort_values(by='porcentaje', ascending=False).head(20)
#Localidades con primera letra en mayúscula
localidad_counts['colloc'] = localidad_counts['colloc'].str.title()

# Display the header using Markdown
st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>¿En qué colonias o localidades se concentra la oferta?</p>", unsafe_allow_html=True)

# Create the bar chart with Plotly Express
fig = px.bar(localidad_counts.sort_values(by='porcentaje', ascending=True),

    x='porcentaje',
    y='colloc',
    orientation='h',
    color='porcentaje',
    color_continuous_scale='YlOrRd',
)
fig.update_layout(
    coloraxis_colorbar=dict(
        title="%",
        
        dtick=3
    ))

# Update the layout of the figure
fig.update_layout(
    showlegend=False,
    yaxis_title=None,  # Removes the y-axis title if desired
    xaxis_title="Porcentaje",  # Customize the x-axis title to represent frequency
 # Ensures the highest value is at the top
 annotations=[
        go.layout.Annotation(
            text='Fuente: Elaboración propia con datos de Goodlers, Inmuebles24, Lamudi y Easybroker',
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            showarrow=False,
            font=dict(
                family='Century Gothic',
                size=12,
                color='grey'
            )
        )
    ]
)

# Render the bar chart in Streamlit
st.plotly_chart(fig)



st.markdown("---")
st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>¿Cómo se distribuyen los precios por zona?</p>", unsafe_allow_html=True)


colloc=df.copy()
#Eliminar registros con colloc en nan
colloc=colloc.dropna(subset=['colloc'])

# Agregar una opción "Total" a las opciones de colloc
unique_colloc = list(colloc['colloc'].unique())
#Ordenar alfabéticamente
unique_colloc.sort()
unique_colloc = ['Total'] + unique_colloc
selected_colloc = st.selectbox('Selecciona una zona', unique_colloc)

# Filtrar los datos basado en la selección
if selected_colloc == 'Total':
    filtered_df = colloc
else:
    filtered_df = colloc[colloc['colloc'] == selected_colloc]

filtered_df["precio_millions"] = filtered_df["precio"] / 1_000_000

# Crear el histograma
fig = px.histogram(filtered_df, x="precio_millions", nbins=20, color_discrete_sequence=['#fca311'])
fig.update_layout(
    xaxis_title="Precio (millones de pesos)",
    yaxis_title="Frecuencia",
    annotations=[
        go.layout.Annotation(
            text='Fuente: Elaboración propia con datos de Goodlers, Inmuebles24, Lamudi y Easybroker',
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            showarrow=False,
            font=dict(
                family='Century Gothic',
                size=12,
                color='grey'
            )
        )
    ]
)

# Mostrar el histograma en la aplicación Streamlit
st.plotly_chart(fig)


st.markdown("---")  

csv = df.to_csv(index=False).encode('utf-8-sig')



st.markdown("---")


st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Amenidades</p>", unsafe_allow_html=True)

# Calculating percentages for the selected colonia
total_amenities = filtered_df[["casa_club", "privada", "cochera", "alberca","paddle", "vigilancia"]].sum().sum()
casa_club_pct = (filtered_df["casa_club"].sum() / total_amenities) * 100
privada_pct = (filtered_df["privada"].sum() / total_amenities) * 100
cochera_pct = (filtered_df["cochera"].sum() / total_amenities) * 100
alberca_pct = (filtered_df["alberca"].sum() / total_amenities) * 100
paddle_pct = (filtered_df["paddle"].sum() / total_amenities) * 100
vigilancia_pct = (filtered_df["vigilancia"].sum() / total_amenities) * 100


fig = px.bar(
    x=["Casa Club", "Privada", "Cochera", "Alberca", "Padel", "Vigilancia"],
    y=[casa_club_pct, privada_pct, cochera_pct, alberca_pct, paddle_pct, vigilancia_pct],
    labels={"x": "Amenidad", "y": "Porcentaje"},
    title=f"Porcentaje de amenidades de {selected_colloc}"
)

# Display the Plotly bar chart in the Streamlit app
st.plotly_chart(fig)

st.markdown("---")


st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Tamaño de las viviendas</p>", unsafe_allow_html=True)



fig = px.histogram(filtered_df, x="mts_const", nbins=20, color_discrete_sequence=['#fca311'])
fig.update_layout(
    title_text=f"Distribución de los metros cuadrados de {selected_colloc}",
    xaxis_title="Metros cuadrados",
    yaxis_title="Frecuencia",
    annotations=[
        go.layout.Annotation(
            text='Fuente: Elaboración propia con datos de Goodlers, Inmuebles24, Lamudi y Easybroker',
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            showarrow=False,
            font=dict(
                family='Century Gothic',
                size=12,
                color='grey'
            )
        )
    ]
)

# Display the Plotly bar chart in the Streamlit app
st.plotly_chart(fig)


# Header
st.markdown("<p style='font-family: Century Gothic; font-weight: bold;font-size: 20px; text-align: center'>Descargar los datos</p>", unsafe_allow_html=True)

# Create a single column layout for the centered button
col1, col2, col3 = st.columns([1,2,1])

with col1:
    st.write("")  # This is just to create a column as a spacer

with col2:
    # Centered download button
    st.download_button(
        label="Descargar los datos del dashboard en formato CSV",
        data=csv,
        file_name='base_de_datos_completa.csv',
        mime='text/csv',
        key='download-csv'
    )

with col3:
    st.write("")  # This is just to create a column as a spacer

# Custom HTML for the centered GIF below the button
st.markdown("<div style='display: flex; justify-content: center;'><img src='https://raw.githubusercontent.com/tylerjrichards/GPT3-Dataset-Generator-V2/main/Gifs/arrow_small_new.gif' width='100'/></div>", unsafe_allow_html=True)

