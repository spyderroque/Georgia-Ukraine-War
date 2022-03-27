"""
# This is the demo app for my private Data Science Project about Georgia:-)

"""

import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px
#import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title = "Demo Data Science Project", layout="wide")
st.write('# Why Georgia sides with Russia in the Ukraine war')
st.markdown("~~ Work in progress. Last updated 17 ^ t h^ / March / 22.~~")

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

st.write("## Demography ")
st.write(" Population estimates for the whole of Georgia by the United Nations.")
# load Data from the UN data repository. Sources must be given in the final app
df_UNdata = pd.read_csv('Demography/UNdata_Export_20220324_103742847.csv')
# Time to wrangle my data
df_UNdata.drop(columns = 'Country or Area', inplace = True)
mylist = []
for x in range(2022,2101) :
    mylist.append(x)
df_UNdata.set_index('Year(s)', inplace = True) #Don't need development to the future
df_UNdata.drop(index = mylist, inplace = True)
df_UNdata.reset_index(inplace = True)
df_UNdata.set_index('Variant', inplace = True)
df_UNdata.drop(index = ['High','Low', 'Constant fertility', 'Instant replacement', 'Instant replacement', 'Zero migration', 'Constant mortality', 'No change', 'Momentum'], inplace = True)
df_UNdata.reset_index(inplace = True)
df_UNdata.rename(columns={'Year(s)': 'Year'}, inplace = True)
df_UNdata.drop(columns = 'Variant', inplace = True)
df_UNdata.rename(columns={'Value': 'Population'}, inplace = True)
df_UNdata['Population'] = df_UNdata['Population']*1000 #correction for the units used in the csv

fig, ax = plt.subplots() 
ax = plt.plot(df_UNdata['Year'], df_UNdata['Population'])
st.pyplot(fig)


st.write("Population data as given by the state of Georgia (Source: https://geostat.ge/media/38040/01---population-by-self-governed-unit.xlsx). Unlike the UN data these data do not include estimates for Abkhazia and South Ossetia. Abkhazia was as a matter of fact never controlled by the Georgian state and South Ossetia is missing after in the last census of 2014.")

df_Population = pd.read_excel('Demography/01---population-by-self-governed-unit.xlsx', header = 3)
mask = df_Population['regions, self-governed units'].str.contains('Municipality')
df_Population.insert(1, 'Municipality', mask, True)
df_Population.at[1,'Municipality'] = False
#These cities are considered as municipality by statisticians
df_Population.at[12,'Municipality'] = True
df_Population.at[30,'Municipality'] = True
df_Population.at[40,'Municipality'] = True
df_Population.at[47,'Municipality'] = True
df_Population.at[53,'Municipality'] = True
df_Population.at[64,'Municipality'] = True
df_Population.at[80,'Municipality'] = True
#drop comments line
df_Population.drop([88,89,90,91], inplace = True)
# let's see how the df_Population table looks like
fig1, ax= plt.subplots()
ax.plot(df_Population.loc[0, 1994:2021])
st.pyplot(fig1)


# Population by region
df_PopReg = df_Population[df_Population['Municipality'] == False]
df_PopReg.drop(columns = 'Municipality', inplace = True)
df_PopReg.set_index('regions, self-governed units', inplace = True)
df_PopReg = df_PopReg.T
df_PopReg.replace(to_replace = '-', value = 0, inplace = True)
df_PopReg.plot(kind = 'line', figsize=(15, 7.5))

#Map to a chloropeth map
df_PopReg2 = df_PopReg.rename(columns = {"C. Tbilisi Municipality":"Tbilisi", "Racha-Lechkhumi and Kvemo Svaneti":"Racha-Lechkhumi-Kvemo Svaneti","Adjara A.R.":"Ajaria"})
df_PopReg2 = df_PopReg2.T
df_PopReg2.reset_index(inplace = True)
df_PopReg2.drop(index = 0, inplace = True) #remove entry "Georgia" in order to improve scale
state_PopReg2 = "geo_regions.geojson"
southossetia = "southossetia.geojson"
MapPop = folium.Map(location=[42.19335024937128, 43.4451901712113], zoom_start=7)
dataStates = df_PopReg2
state_data=pd.DataFrame.from_dict(dataStates)
year_value = st.slider('Choose year', 1994,2021,2021)
bins = [0,300, 601, 902, 1203]
folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=state_data,
    columns=["regions, self-governed units", year_value],
    key_on="feature.properties.NAME_1",
    fill_color= "YlOrRd",
    fill_opacity=0.5,
    line_opacity=0.2,
    nan_fill_color="blue",
    nan_fill_opacity = 0.2,
    legend_name="Population by Region",
    bins = bins
).add_to(MapPop)

folium.GeoJson(
    southossetia,#fill_opacity=1.0, 
    name="geojson"
).add_to(MapPop)
folium_static(MapPop)


st.write("### Methodology")
st.write(" Lorem ipsum dolor...")
st.write("## Economics ")
st.write("### Methodology")
st.write(" Lorem ipsum dolor...")
st.write("### Import and export")
st.write(" Lorem ipsum dolor...")
st.write("### FDI and remissions")
st.write(" Lorem ipsum dolor...")
st.write("## Summary and Conclusion")
st.write("## Sources")
