####################################
# 
# APPLIED DATA SCIENCE WITH PYTHON
# COURSE 2 - DATA VISUALISATION
# WEEK 4 - CAPSTONE PROJECT
#
# By Thierry Gagne
# Started Feb 23rd, 2023 
#
# PART 1 - EXTRACTING THE DATA
#
####################################

####################################
# TASK
####################################

# This assignment requires that you to find **at least two datasets** on the web which are related, 
# and that you visualize these datasets to answer a question with the broad topic of **sports or athletics**.

# Instructions:

    # * You must state a question you are seeking to answer with your visualizations.
    # * You must provide at least two links to available datasets. 
    # * You must upload an image which addresses the research question you stated. 
    # * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.

####################################
# RESEARCH QUESTION
####################################

# Is the number of sports facilities in a Montreal borough associated with its inhabitants' satisfaction with the city?

####################################
# STRATEGY
####################################

# 1. Extract and clean two datasets - for sports facilities and inhabitants' satisfaction. 

# 1. Make a choropleth map of Montreal boroughs with:
    # Dots representing sports facilities
    # Polygons of colors for boroughs and their average satisfaction levels.

# 2. Make a bar chart with the count of sports facilities by borough, 
    # with an extra line representing its association with average satisfaction levels across boroughs.

####################################
# DATA
####################################

# 1. Sports installations
# URL: https://donneesquebec.ca/recherche/dataset/vmtl-installations-recreatives-sportives-et-culturelles

# 2. Satisfaction with the city
# URL: https://donneesquebec.ca/recherche/dataset/vmtl-sondage-satisfaction-citoyens

####################################
# CODE
####################################

# Printing an introduction
print("\nWelcome! This code accesses three datasets online, so have some patience :)")
print("It crashed on me once, so just try running it again if it happens. \n")

url1 = 'https://data.montreal.ca/dataset/60850740-dd83-47ee-9a19-13d674e90314/resource/2dac229f-6089-4cb7-ab0b-eadc6a147d5d/download/terrain_sport_ext.json'
url2 = 'https://data.montreal.ca/dataset/4656e09e-001d-4ad3-95de-67235310ecb7/resource/998f72da-3819-4058-9e24-5df42d2197ad/download/resultatssondagesatisfactioncollectifs2016.csv'
url3 = 'https://data.montreal.ca/dataset/9797a946-9da8-41ec-8815-f6b276dec7e9/resource/6b313375-d9bc-4dc3-af8e-ceae3762ae6e/download/limites-administratives-agglomeration-nad83.geojson'
print("URL 1:\n" + str(url1))
print("\nURL 2:\n" + str(url2)) 
print("\nURL 3:\n" + str(url3)) 
print("")

# Import libraries
import ssl
import urllib.request
import json
import numpy as np
import pandas as pd
import folium
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

########################
# Open SPORTS dataset
########################

print("!!! Accessing the SPORTS dataset online... \n")
fileobj_raw = urllib.request.urlopen(url1, context = ctx)
fileobj_clean = fileobj_raw.read().decode("UTF-8")                                 # This creates a string class instance 
js = json.loads(fileobj_clean)

# DEBUG 1 - Just want to print the good parts.
    # print(json.dumps(js, indent=4))

# Create list variables from this:
listname = []
listtype = []
listborough = []
listcoordinates = []
listlongitude = []
listlatitude = []

for x in js["features"]:
    listname.append(x["properties"]["NOM"])
    listtype.append(x["properties"]["TYPE"])
    listborough.append(x["properties"]["ARROND"])
    listcoordinates.append(x["geometry"]["coordinates"])

for x in listcoordinates:
    listlongitude.append(x[0])
    listlatitude.append(x[1])

# Create SPORTS DataFrame
print("Printing top 10 entries... \n")
df = pd.DataFrame([listname, listtype, listborough, listlongitude, listlatitude])
df = df.T
df.columns = ["name", 'type', 'borough', 'longitude', 'latitude']
df_sports = df[df["type"] == "Sportif"]
df1 = df_sports.reset_index(drop=True)
df1['longitude'] = df1['longitude'].astype(float)
df1['latitude'] = df1['latitude'].astype(float)
count = pd.Series(df1.groupby(['borough'])["longitude"].count())
print("Printing the number of sport facilities across boroughs... \n")
print(count)
df1 = df1.merge(count, how='inner', on='borough')
df1.columns = ["name", 'type', 'borough', 'longitude', 'latitude', 'count']
print("\nPrinting the top 10 rows... \n")
print(df1.head(10))
print("\n There are {} sports facilities in this dataset".format(len(df1)))

########################
# Open SATISFACTION dataset
########################

print("\n!!! Accessing the SATISFACTION dataset online... \n")

df2 = pd.read_csv('https://data.montreal.ca/dataset/4656e09e-001d-4ad3-95de-67235310ecb7/resource/998f72da-3819-4058-9e24-5df42d2197ad/download/resultatssondagesatisfactioncollectifs2016.csv', usecols = ['Q3','QNPS'])
df2.columns = ["borough", "satisfaction"]

def update_borough(x):
    if x == 1:
        return "Ahuntsic-Cartierville"
    if x == 2:
        return "Anjou"
    if x == 3:
        return "Côte-des-Neiges-Notre-Dame-de-Grâce"
    if x == 4:
        return "Lachine"
    if x == 5:
        return "LaSalle"
    if x == 6:
        return "L'Île-Bizard-Sainte-Geneviève"
    if x == 7:
        return "Mercier-Hochelaga-Maisonneuve"
    if x == 8:
        return "Montréal-Nord"
    if x == 9:
        return "Outremont"
    if x == 10:
        return "Pierrefonds-Roxboro"
    if x == 11:
        return "Plateau-Mont-Royal"
    if x == 12:
        return "Rivière-des-Prairies-Pointe-aux-Trembles"
    if x == 13:
        return "Rosemont-La Petite-Patrie"
    if x == 14:
        return "Saint-Laurent"
    if x == 15:
        return "Saint-Léonard"
    if x == 16:
        return "Sud-Ouest"
    if x == 17:
        return "Verdun"
    if x == 18:
        return "Ville-Marie"
    if x == 19:
        return "Villeray-Saint-Michel-Parc-Extension"
    if x == 20 | x == 99:
        return None

df2["borough"] = df2["borough"].apply(lambda x: update_borough(x))

df2["satisfaction"] = df2["satisfaction"].astype(int)
def clean_satisfaction(x):
    if x == 98:
        return None
    if x == 99:
        return None
    else:
        return x
df2["satisfaction"] = df2["satisfaction"].apply(lambda x: clean_satisfaction(x))
avgsat = pd.Series(df2.groupby(["borough"])["satisfaction"].mean())
print("Printing average satisfaction scores across boroughs... \n")
print(avgsat)

df2 = df2.merge(avgsat, how='inner', on='borough')
df2.columns = ['borough', 'satisfaction', 'avgsat']

print("\nPrinting the top 10 rows... \n")
print(df2.head(10))
print("\n There are {} responses in this dataset".format(len(df2)))

########################
# Open POLYGONS dataset
########################

import geopandas as gpd

print("\n!!! Accessing the POLYGONS dataset online... \n")
df3 = gpd.read_file(url3)
df3 = df3.to_crs(epsg=4326)

# fileobj_raw = urllib.request.urlopen(url3, context = ctx)
# fileobj_clean = fileobj_raw.read().decode("UTF-8")                                 # This creates a string class instance 
# js = json.loads(fileobj_clean)

# listborough = []
# listmultipolygon = []

# for x in js["features"]:
#     listborough.append(x["properties"]["NOM"])
#     listmultipolygon.append(x["geometry"]["coordinates"])

# print("Printing example... \n")
# df3 = pd.DataFrame([listborough, listmultipolygon])
# df3 = df3.T
# df3.columns = ["borough", 'multipolygon']

df3["borough"] = df3["NOM"]
df3 = df3.drop(['CODEID', 'NOM_OFFICIEL', 'CODEMAMH', 'CODE_3C', 'NUM', 'TYPE', 'COMMENT', 'DATEMODIF'], axis=1)
df4 = pd.merge(df3, count, on=['borough'])
df4["count"] = df4["longitude"]
df4 = df4.drop(["longitude"], axis=1)
df4 = pd.merge(df4, avgsat, on=['borough'])
df4 = df4.drop(['borough'], axis=1)
df4['satisfaction'] = df4['satisfaction'].astype(float)
print(df4.sort_values(by = "satisfaction").head(17))
print("\n There is data on {} boroughs, including {} with data on sports facilities and satisfaction scores.".format(len(df3), len(df4)))

########################
# CREATING FOLIUM MAP
########################

# 3.1. Adding the sports facilities' coordinates

print("\nProducing the Folium Map...\n")    
meanlat = df1["latitude"].mean()
meanlon = df1["longitude"].mean()

print("Mean latitude: " + str(meanlat))
print("Mean longitude: " + str(meanlon))

print("\nPlease wait a bit...") 
map = folium.Map(location=[meanlat, meanlon])
for x in range(len(df1)):
    folium.Marker(
        [df1["latitude"][x], df1["longitude"][x]], 
        popup=df1['name'][x]).add_to(map)

# 3.2 Add polygons to represent Montreal boroughs

for _, r in df4.iterrows():
    # Without simplifying the representation of each borough,
    # the map might not be displayed
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j)
    folium.Popup(r['NOM']).add_to(geo_j)
    geo_j.add_to(map)


# df = gpd.read_file(gpd.datasets.get_path(url3))
# dfchoro = df.to_crs(epsg=4326)

folium.Choropleth(
    geo_data=df3,
    name="choropleth",
    data=df4,
    columns=["NOM", "satisfaction"],
    key_on="feature.properties.NOM",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Satisfaction (1-10)",
).add_to(map)

map.save("map.html")

########################
# ADD BAR CHART
########################

print("\nSaving the bar chart...") 

import matplotlib.pyplot as plt
from scipy import stats
res = stats.spearmanr(df4["satisfaction"], df4["count"])
stat = round(res.statistic, 3)
pvalue = round(res.pvalue, 3)

plt.figure(figsize=(20, 10))
df4 = df4.sort_values(by = "satisfaction")
plt.bar(df4["NOM"], df4["satisfaction"]*10, label="Satisfaction")
plt.scatter(df4["NOM"], df4["count"], label="Sports facilities")
xlabellist = ["LC", "IS", "MN", "RP", "PR", "LN", "LS", "AC", "RO", "MH", "VM", "LR", "AJ", "VD",
        "VS", "CN", "OM"]
plt.xticks(df4["NOM"], xlabellist, rotation=45, ha='right', fontsize=8)
plt.title("Number of sports facilities and average satisfaction (10-100) across 17 Montreal boroughs")
plt.legend(frameon=False)
txt="Question: \"What is the probability that you would recommend living in Montreal to a friend?\" "
txt2="Number of facilities varied from 13 (Outremont) to 80 (RDP-PAT)"
txt3="Satisfaction varied from 7.23 (Lachine) to 8.07 (Outremont)"
txt4="Spearman Rho correlation coefficient: r = {}, p = {}".format(stat, pvalue)
plt.figtext(0.5, 0.055, txt, wrap=True, horizontalalignment='center', fontsize=8)
plt.figtext(0.5, 0.04, txt2, wrap=True, horizontalalignment='center', fontsize=8)
plt.figtext(0.5, 0.025, txt3, wrap=True, horizontalalignment='center', fontsize=8)
plt.figtext(0.5, 0.01, txt4, wrap=True, horizontalalignment='center', fontsize=8)
plt.savefig('figure_20_10.png', bbox_inches='tight')
# plt.show()

########################
# END
########################

print("\n!!! Done!\n")

####################################
# RESOURCES
####################################

# 1. Making a random-effects model in Python
# URL: https://www.pythonfordatascience.org/mixed-effects-regression-python/

# 2. Putting polygons in Folium
# URL: https://geopandas.org/en/stable/gallery/polygon_plotting_with_folium.html

# 3. Opening GeoJSON files straight from GeoPandas
# URL: https://docs.astraea.earth/hc/en-us/articles/360043919911-Read-a-GeoJSON-File-into-a-GeoPandas-DataFrame
