"""
# This is the demo app for my private Data Science Project about Georgia:-)

"""

from turtle import window_width
import streamlit as st
import pandas as pd
from pandas import IndexSlice as idx
import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

idx = pd.IndexSlice

st.set_page_config(page_title = "Demo Data Science Project", layout="wide")
st.write('# Why Georgia sides with Russia in the Ukraine war')
st.markdown("~~ Work in progress. Last updated 09th / April / 22.~~")

st.markdown(" ***In 2008 Georgia faced an invasion by Russia in a war with striking similarity to the present invasion of Ukraine. Since then one-fifth of the country is occupied by Russian troops. Russia's president Vladimir Putin left no doubt that he intends to fully annex the former soviet state next. The invasion of Georgia in 2008 was stopped due to an intervention by the presidents of Ukraine and USA. Yet, in the present war Georgia has not sided with the Ukraine claiming that a participation in international sanctions would lead to economic and social collapse. Is this true or is the acting Georgian government just a puppet regime in the pocket of Vladimir Putin? This private data science projects is trying shed light into this question.***")
st.image("pexels-genadi-yakovlev-4550542.jpg")
st.write("Source: https://images.pexels.com/photos/4550542/pexels-photo-4550542.jpeg?cs=srgb&dl=pexels-genadi-yakovlev-4550542.jpg&fm=jpg")

st.write(" ## Georgia? Where is that?")
st.write(" Until fairly recently Georgia was for me just yet another obscure post-soviet era statelet somewhere in the east within the russian sphere of influence. With increasing tensions between Ukraine and Russia, which sadly has turned into a war, international politics have turned their focus to Georgia.")

MapGe1 = folium.Map(location=[41.94860908784443, 44.3235798039364], zoom_start=6, tiles='Stamen Terrain')
folium_static(MapGe1)

st.write("Located north of Turkey and the Middle East, Georgia lies at Europe's eastern fringe connecting Europe and Asia. It does not take much to imagine that along its fertile western shoreline some of the first humans settled in Europe. Most notably wine is native to Georgia and thus it is little wonder that the oldest traces of domisticated wine grapes, dated 6000 BCE, have been found there [1, 2]. ")
st.markdown(" In 2008 Russia provoked and then occupied 20 '%' of Georgia under the pretense of protecting Russian citizens from oppression in South Ossetia and Abkhazia. A pattern which repeated itself in Syria and Ukraine 2014 and today. [3-5] The eastern statelet, marked red, is the province of Abkhazia, the blue marked territory calls itself South Ossetia. According to [6] the Georgian state never held control over these two territories after its seccession from the USSR, as an aftermath of the Georgian civil war.")

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
st.write(" Population estimates for the whole of Georgia.")
# load Data from the UN data repository. Sources must be given in the final app
df_UNdata = pd.read_pickle('Demography/df_UNdata.pkl')
# load Data from the Geostat data repository Georgia total and by regions are given in this table. Sources must be given in the final app
df_PopReg = pd.read_pickle('Demography/df_PopReg.pkl')


fig = go.Figure()
fig.add_trace(go.Scatter(x=df_UNdata['Year'], y=df_UNdata['Population'],
                    mode='lines',
                    name='UN estimations for Georgia incl. Abkhazia and South Ossetia'))
fig.add_trace(go.Scatter(x=df_PopReg.index.values, y=df_PopReg['Georgia']*1000,
                    mode='lines',
                    name='Georgian estimates excl. Abkhazia and South Ossetia'))
markerPosT_UN = [1959, 1970,1979, 1989]
markerPosT_Ge = [1994,2002, 2014]
markerYT_UN = [3.9412*10**6, 4.713342*10**6,4.985588*10**6, 5.411993*10**6]
markerYT_Ge = [4.9299*10**6, 3.991273*10**6, 3.716911*10**6]
fig.add_trace(go.Scatter(x=markerPosT_UN, y = markerYT_UN, mode = 'markers', marker_color='blue', showlegend= False))
fig.add_trace(go.Scatter(x=markerPosT_Ge, y = markerYT_Ge, mode = 'markers', marker_color='red', showlegend=False))
st.plotly_chart(fig, use_container_width=True)

st.write("Population data as given by the state of Georgia (Source: https://geostat.ge/media/38040/01---population-by-self-governed-unit.xlsx). Unlike the UN data these data do not include estimates for Abkhazia and South Ossetia. Abkhazia was as a matter of fact never controlled by the Georgian state and South Ossetia is missing in the estimates from 2008 onward (i.e. census of 2014.) The markings indicate values gained in a census. The long gap between the censi 1989 and 2002 reflects a period of transition. Between 1991 and the mid 90s Georgia was occupied with its secession from the USSR / Russia and then years of civil war.")
st.write(" For the pupose of this project I will use the estimations of the Georgian state in which South Ossetia and Abkhazia are not properly considered.")
st.write("The following chloropeth and area chart show the evolution of the population in each region of Georgia.")

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
bins = [0,100, 300, 500, 700, 900, 1100, 1300]
folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=state_data,
    columns=["regions, self-governed units", year_value],
    key_on="feature.properties.NAME_1",
    fill_color= "YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    nan_fill_color="blue",
    nan_fill_opacity = 0.2,
    legend_name="Population by Region (in thousand)",
    bins = bins
).add_to(MapPop)

folium.GeoJson(
    southossetia,#fill_opacity=1.0, 
    name="geojson"
).add_to(MapPop)
folium_static(MapPop)


fig30 = go.Figure()
#fig30.add_trace(go.Scatter(x=df_PopReg.index.values, y=df_PopReg['Georgia']*1000,
#                    mode='lines',fill='tozeroy', name='Georgia total'))
dicttemp = {}
for count, value in enumerate(df_PopReg.columns.values):
    dicttemp[count] = value
for value in range(1,len(dicttemp)):
    fig30.add_trace(go.Scatter(x=df_PopReg.index.values, y=df_PopReg[dicttemp[value]]*1000,
                    mode='lines',fill='tonexty', name=dicttemp[value], stackgroup='one'))
fig30.update_layout(height = 750)
st.plotly_chart(fig30, use_container_width=True)


df_PopAgeSex = pd.read_pickle('Demography/df_PopAgeSex.pkl')
fig10 = go.Figure()
fig10.add_trace(go.Bar(y = df_PopAgeSex.index.values, x = df_PopAgeSex.loc[idx[:,(2021, "Males")]], 
                       name = 'Male', orientation = 'h'))
fig10.add_trace(go.Bar(y = df_PopAgeSex.index.values, x = (-1)*df_PopAgeSex.loc[idx[:,(2021, "Females")]], 
                       name = 'Female', orientation = 'h'))

# Updating the layout for our graph
fig10.update_layout(title = 'Population Pyramid of Georgia (2021)',
                 title_font_size = 22, barmode = 'relative',
                 bargap = 0.0, bargroupgap = 0,
                 xaxis = dict(tickvals = [-30000, -20000, -10000,
                                          0, 10000, 20000, 30000],
                                
                              ticktext = ['30k', '20k', '10k', '0', 
                                          '10k', '20k', '30k'],
                                
                              title = 'Population',
                              title_font_size = 14),
                 height=750
                 )
#fig10.add_hrect(y0=29, y1=46, line_width=0, fillcolor="yellow", opacity=0.3)
fig10.add_hline(y=46, line_width = 2, line_dash = "dash", line_color = "black")
fig10.add_hline(y=29, line_width = 2, line_dash = "dash", line_color = "black")
st.plotly_chart(fig10, use_container_width=True)

st.write("Not withstanding the decrease of population the above charts do not show anything remarkable to the question at hand. The population pyramid,however, gives us some interesting clues. Georgia has a rather young population compared to most western European societies. The black line in the pyramid indicates the age group which was 15 years of age at the abolishion of the USSR in 1991. The assumption is made that this age group and the groups below the black line don't have any significant experiences of life in USSR or Russia. The white line is the age group which was 15 years of age during the Russian-Georgian war in 2008 and therefore have no or a limited memory of the pre-war period. This information is vital as the standard of living dropped significantly after seccession from the USSR.") 
st.write("The final chapter of the post-soviet era closed only in 2002 when former soviet minister of foreign affairs and president of Georgia, Eduard Shevardnaze, was ousted from his office during the so called 'rose revolution'. The succeding government made substantial changes towards a liberal market economy and focus towards western countries.[6] ")

st.write("### Methodology")
st.write("In this section we took an initial look at Georgia and its demography. The data source for the population estimates can be found on the the website of the UN database http://data.un.org. The population estimates of the Georgian states are found under https://geostat.ge/media/38040/01---population-by-self-governed-unit.xlsx. The data about ethnicity is found under  http://census.ge/files/results/english/17_Total%20population%20by%20regions%20and%20ethnicity.xls. Asa there seems to be inconsistencies in latter file. I web scraped https://en.wikipedia.org/wiki/Demographics_of_Georgia_(country) on 02/04/2022.")

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
st.write('[1] https://www.nationalgeographic.com/travel/article/sponsor-content-secret-birthplace-of-wine last checked on 21/03/2022')
st.write('[2] https://www.bbc.com/news/world-europe-41977709 last checked on 22/03/2022')
st.write('[3] https://www.nytimes.com/2022/03/19/world/europe/ukraine-georgia-war.html last checked on 22/03/2022')
st.write('[4] https://www.crisisgroup.org/europe-central-asia/caucasus/georgia/ukraine-georgia-sees-powerful-and-worrying-parallels last checked on 19/03/2022')
st.write('[5] https://zdfheute-stories-scroll.zdf.de/putin-kriege-ukraine/index.html')
st.write('[6] Acemoglu, D. and Robinson, J.A.; The Narrow Corridor - States, Societies, and the Fate of Liberty, Pinguin Press, 2019')
st.write('[7] ')
st.write('[8] ')
st.write('[9] ')
st.write('[10] ')
st.write('[11] ')
st.write('[12] ')

df_EthnicityTime = pd.read_pickle('Demography\df_EthnicityTime.pkl')
df_EthnicityTime
