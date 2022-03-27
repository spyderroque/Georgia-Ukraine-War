"""
# This is the demo app for my private Data Science Project about Georgia:-)

"""

import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px
#import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title = "Demo Data Science Project", layout="wide")
st.write('# Why Georgia sides with Russia in the Ukraine war')
st.markdown(" ***In 2008 Georgia faced an invasion by Russia in a war with striking similarity to the present invasion of Ukraine. Since then one-fifth of the country is occupied by Russian troops. Russia's president Vladimir Putin left no doubt that he intends to fully annex the former soviet state next. The invasion of Georgia in 2008 was stopped due to an intervention by the presidents of Ukraine and USA. Yet, in the present war Georgia has not sided with the Ukraine claiming that a participation in international sanctions would lead to economic and social collapse. Is this true or is the acting Georgian government just a puppet regime in the pocket of Vladimir Putin? This private data science projects is trying shed light into this question.***")
st.image("https://images.pexels.com/photos/4550542/pexels-photo-4550542.jpeg?cs=srgb&dl=pexels-genadi-yakovlev-4550542.jpg&fm=jpg")
st.write("Source: https://images.pexels.com/photos/4550542/pexels-photo-4550542.jpeg?cs=srgb&dl=pexels-genadi-yakovlev-4550542.jpg&fm=jpg")

st.write(" ## Georgia? Where is that?")
st.write(" Until fairly recently Georgia was for me just yet another obscure post-soviet era statelet somewhere in the east within the russian sphere of influence. With increasing tensions between Ukraine and Russia, which sadly has turned into a war, international politics have turned their focus to Georgia.")

MapGe1 = folium.Map(location=[41.94860908784443, 44.3235798039364], zoom_start=6, tiles='Stamen Terrain')
folium_static(MapGe1)

st.write("Located north of Turkey and the Middle East, Georgia lies at Europe's eastern fringe connecting Europe and Asia. It does not take much to imagine that along its fertile western shoreline some of the first humans settled in Europe. Most notably wine is native to Georgia and thus it is little wonder that the oldest traces of domisticated wine grapes, dated 6000 BCE, have been found there [1, 2]. ")
st.markdown(" In 2008 Russia provoked and then occupied 20 '%' of Georgia under the pretense of protecting Russian citizens from  oppression. A pattern which repeated itself in Syria and Ukraine 2014 and today. [3-5] The eastern statelet, marked red, is the province of Abkhazia, the blue marked territory calls itself South Ossetia. ")

# Download GeoJson of Abchasia
state_geo = "geo_regions.geojson"
southossetia = "southossetia.geojson"
MapGe2 = folium.Map(location=[41.94860908784443, 44.3235798039364], zoom_start=7)

dataStates = {'State': ["Abkhazia", "Ajaria"], 'value': [1, 0]}
state_data=pd.DataFrame.from_dict(dataStates)

folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=state_data,
    columns=["State", "value"],
    key_on="feature.properties.NAME_1",
    fill_color="OrRd",
    fill_opacity=0.3,
    line_opacity=0.2,
    nan_fill_color="black",
    nan_fill_opacity = 0.1,
    legend_name="Occupied Territories",
).add_to(MapGe2)

folium.GeoJson(
    southossetia, 
    name="geojson"
).add_to(MapGe2)
folium_static(MapGe2)