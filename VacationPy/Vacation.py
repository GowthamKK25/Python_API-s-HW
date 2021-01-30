#!/usr/bin/env python
# coding: utf-8

# In[97]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress
import gmaps
# Import API key
from api_keys import gkey
import json

# Incorporated weather Data into dataframe
CityDataFrame = pd.read_csv('weather_dataframe.csv') 


# In[98]:


#Visual
CityDataFrame.reset_index()  
CityDataFrame = CityDataFrame.drop(columns={'Unnamed: 0'}) 
CityDataFrame.head()


# In[99]:


#Gmap to Gkey
gmaps.configure(api_key=gkey)


# In[100]:


#Base Humidity Map
locations = CityDataFrame[["Lat", "Lng"]].astype(float) 
Humidity = CityDataFrame['Humidity'].astype(float) 
fig = gmaps.figure()

heat_layer = gmaps.heatmap_layer(locations, weights=Humidity, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = 1)

fig.add_layer(heat_layer)

fig


# In[ ]:


#Setting conditions for ideal weather
IdealWeather = CityDataFrame.loc[CityDataFrame["MaxTemp"] < 80 ] 
IdealWeather =  CityDataFrame.loc[CityDataFrame["MaxTemp"] > 70 ]  
IdealWeather = CityDataFrame.loc[CityDataFrame["WindSpeed"] < 10]   
IdealWeather = CityDataFrame.loc[CityDataFrame["Cloudiness"]  == 0]    
IdealWeather = IdealWeather.drop(columns = {'Unnamed: 0'}) 
IdealWeather.dtypes 
IdealWeather = IdealWeather.dropna() 
IdealWeather


# In[102]:


#New Locations and Humidity
locations = IdealWeather[["Lat", "Lng"]].astype(float)  
Humidity = IdealWeather['Humidity'].astype(float) 


# In[103]:


#Specfied Heat Map with ideal weather
fig = gmaps.figure()

heat_layer = gmaps.heatmap_layer(locations, weights=Humidity, 
                                 dissipating=False, max_intensity=100,
                                 point_radius = 1)

fig.add_layer(heat_layer)

fig


# In[108]:


# Finding hotels for each location with iterrows
params = {
    "radius": 5000,
    "types": "hotel",
    "keyword": "hotel",
    "key": gkey
}

# Use the lat/lng to find hotel nearby
for index, row in IdealWeather.iterrows():
    # get lat, lng from df
    lat = row["Lat"]
    lng = row["Lng"]

    # change location each iteration while leaving original params in place
    params["location"] = f"{lat},{lng}"

    # Params and our lat/lng
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # make request and print url
    name_address = requests.get(base_url, params=params)
    
#     print the name_address url, avoid doing for public github repos in order to avoid exposing key
#     print(name_address.url)

    # convert to json
    name_address = name_address.json()
    # print(json.dumps(name_address, indent=4, sort_keys=True))

    # Since some data may be missing we incorporate a try-except to skip any that are missing a data point.
    try:
        IdealWeather.loc[index, "Hotel Name"] = name_address["results"][0]["name"]
    except (KeyError, IndexError):
        print("oops")


# In[ ]:


#Infobox code
info_box_template = """
<dl>
<dt>Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{city name}</dd>
<dt>Country</dt><dd>{country}</dd>
</dl>
"""


# In[ ]:


# Store the DataFrame Row
# NOTE: be sure to update with your DataFrame name
hotel_info = [info_box_template.format(**row) for index, row in IdealWeather.iterrows()]
locations = hotel_df[["Lat", "Lng"]]


# In[113]:


#Hotel map
hotel_layer = gmaps.symbol_layer(
    locations, fill_color='rgba(0, 150, 0, 0.4)',
    stroke_color='rgba(0, 0, 150, 0.4)', scale=2,
    info_box_content=[info_box_template.format(**row) for index, row in IdealWeather.iterrows()]
) 
fig = gmaps.figure()
fig.add_layer(hotel_layer)
fig.add_layer(heat_layer)
fig


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




