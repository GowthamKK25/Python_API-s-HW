#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress

# Import API key
from api_keys import weather_api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy


# In[2]:


# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180) 


# In[3]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
lngs = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# In[4]:


#Lists to be filled with values
url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" + weather_api_key 
diffcity = []
Lat = []
Lng = []
MaxTemp = []
Humidity = []
Cloudiness = []
WindSpeed = []
Date = [] 
country = []


# In[5]:


#Loops on Json object to get data and put into lists
numcounter = 0
setcounter = 0

for city in cities:    
    query = url + "&q=" + city
    response = requests.get(query)
    response_json = response.json()
    
    if numcounter < 50:
        numcounter += 1
    else: 
        setcounter += 1
        numcounter = 0
    print(f'Processing Record {numcounter} in set {setcounter} for city {city}')
    try:   
        Lat.append(response_json['coord']['lat']) 
        Lng.append(response_json['coord']['lon']) 
        MaxTemp.append(response_json['main']['temp_max']) 
        Humidity.append(response_json['main']['humidity'])
        Cloudiness.append(response_json['clouds']['all'])  
        WindSpeed.append(response_json['wind']['speed']) 
        Date.append(response_json['dt'])  
        country.append(response_json['sys']['country']) 
        diffcity.append(city) 
    except: 
        print('city not found') 
        pass


# In[6]:


#Create csv from print data
weather_dict = {'city name':diffcity, 
'Lat': Lat,
'Lng': Lng,
'MaxTemp': MaxTemp,
'Humidity':Humidity,
'Cloudiness': Cloudiness,
'WindSpeed': WindSpeed,
'Date' : Date,
'country' : country} 

weather_dataframe = pd.DataFrame(weather_dict) 
weather_dataframe 
weather_dataframe.to_csv("weather_dataframe.csv")


# In[7]:


#Visual
weather_dataframe


# In[49]:


# The following plot is measuring the the temperature on the x axis 
# and the Latitude on the y axis, there seems to be somewhat of a relation between the two vairables with .58 as the r^2
x_values = weather_dataframe['MaxTemp']
y_values = weather_dataframe['Lat']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('MaxTemp')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("Temp v Lat")
plt.show()  
plt.savefig("MaxTemp.png")


# In[50]:


# The following plot is measuring the relation between humidity and latitude, of which there seems to be little
x_values = weather_dataframe['Humidity']
y_values = weather_dataframe['Lat'] 
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('Humidity')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("Humidity v Lat")
plt.show() 
plt.savefig("Humidity.png")


# In[51]:


# The following shows the relation of Cloudniness and Latitude, at there seems to be lttile
x_values = weather_dataframe['Cloudiness']
y_values = weather_dataframe['Lat'] 
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('Lat')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("Cloudiness v Lat")
plt.show() 
plt.savefig("Cloudiness.png")


# In[52]:


# The following graphy shows the relation between Wind Speed and Lat, of which there is little
x_values = weather_dataframe['WindSpeed']
y_values = weather_dataframe['Lat'] 
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('WindSpeed')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("WindSpeed v Lat")
plt.show() 
plt.savefig("WindSpeed.png")


# In[12]:


# North and South Dataframes
NorthHemishphere = weather_dataframe.loc[weather_dataframe['Lat'] >= 0]
SouthHemisphere = weather_dataframe.loc[weather_dataframe['Lat'] <= 0]


# In[13]:


#North Hemisphere Temp
x_values = NorthHemishphere['MaxTemp']
y_values = NorthHemishphere['Lat']


# In[53]:


#Little to no assoication because r^2 is low
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('MaxTemp')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("NH Temp v Lat")
plt.show()  
plt.savefig("NHMaxTemp.png")


# In[54]:


#South Hemisphere Temp, Low association as well because r^2 is low
x_values = SouthHemisphere['MaxTemp']
y_values = SouthHemisphere['Lat']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('MaxTemp')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("SH Temp v Lat")
plt.show()  
plt.savefig("SHMaxTemp.png")


# In[55]:


# North Hemisphere Humidity, low assoication because r^2 is low between the values
x_values =  NorthHemishphere['Humidity']
y_values = NorthHemishphere['Lat']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('Humidity')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("NH Humidity v Lat")
plt.show()  
plt.savefig("NHHumidity.png")


# In[56]:


#South Hemisphere Humidity, very low association due to low r^2
x_values =  SouthHemisphere['Humidity']
y_values = SouthHemisphere['Lat']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('Humidity')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("SH Humidity v Lat")
plt.show() 
plt.savefig("SHHumidity.png")


# In[57]:


#North Hemisphere Cloudiness, low r^2 so low association between variables
x_values =  NorthHemishphere['Cloudiness']
y_values = NorthHemishphere['Lat']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('Humidity')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("NH Cloudiness v Lat")
plt.show()  
plt.savefig("NHCloudiness.png")


# In[58]:


#South Hemisphere Cloudiness, low assoication and low r^2
x_values =  SouthHemisphere['Cloudiness']
y_values = SouthHemisphere['Lat']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('Humidity')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("SH Cloudiness v Lat")
plt.show() 
plt.savefig("SHCloudiness.png")


# In[59]:


#North Hemisphere Wind Speed, very low association between variables
x_values =  NorthHemishphere['WindSpeed']
y_values = NorthHemishphere['Lat']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('Wind Speed')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("NH WindSpeed v Lat")
plt.show()  
plt.savefig("NHwindspeed.png")


# In[61]:


#South Hemisphere Wind Speed,low association
x_values =  SouthHemisphere['WindSpeed']
y_values = SouthHemisphere['Lat']
(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(6,10),fontsize=15,color="red")
plt.xlabel('Wind Speed')
plt.ylabel('Lat')
print(f"The r-squared is: {rvalue**2}")
plt.title("SH WindSpeed v Lat")
plt.show() 
plt.savefig("SHwindspeed.png")


# In[ ]:





# In[ ]:





# In[ ]:




