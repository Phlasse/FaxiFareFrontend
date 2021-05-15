import streamlit as st
import datetime
import requests
#import joblib
import geopy
#import geocoder
#import folium
import pandas as pd
#import numpy as np
from geopy.geocoders import Nominatim
import warnings
warnings.filterwarnings("ignore")
import pydeck as pdk

def get_latlo(address):
    geolocator = Nominatim(user_agent="fed-up")
    location = geolocator.geocode(address)
    loc_stats = (location.latitude, location.longitude)
    return loc_stats

NYC_center_lat = 40.7408648
NYC_center_lon = -74.
st.subheader("Fed-up TaxiFare Calculator")
startingpoint = st.sidebar.text_input("Where does your Journey start?", "Empire state building")
start_point = get_latlo(startingpoint)
st.sidebar.text(start_point)
endingpoint = st.sidebar.text_input("Where do you want to go?", "Chrysler building")
end_point = get_latlo(endingpoint)
st.sidebar.text(end_point)
pax_count =  st.sidebar.slider("How many passengers?",1,8, 2)
time_var = st.sidebar.time_input("When do you want to take a taxi?", value=datetime.datetime(2021, 10, 6, 12, 10, 20))

data = pd.DataFrame({
    'awesome cities' : ["Start", "End"],
    'lat' : [start_point[0], end_point[0]],
    'lon' : [start_point[1], end_point[1]]
})

st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=NYC_center_lat,
            longitude=NYC_center_lon,
            zoom=10,
            pitch=50,
         ),
         layers=[
             pdk.Layer(
                'ScatterplotLayer',
                filled= True,
                radiusMinPixels= 4,
                data=data,
                get_position='[lon, lat]',
                get_fill_color='[33, 133, 233]',
             )],))

key = '2012-10-06 12:10:20.0000001'
pickup_date = st.sidebar.date_input('pickup datetime', value=datetime.datetime(2021, 10, 6, 12, 10, 20))
pickup_datetime = f'{pickup_date} {time_var}UTC'
pickup_longitude = start_point[1]
pickup_latitude = start_point[0]
dropoff_longitude = end_point[1]
dropoff_latitude = end_point[0]
passenger_count = pax_count

url = 'https://taxiapi-pude6ihnsq-ew.a.run.app/predict_fare'
params = dict(
    key=key,
    pickup_datetime=pickup_datetime,
    pickup_longitude=pickup_longitude,
    pickup_latitude=pickup_latitude,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude=dropoff_latitude,
    passenger_count=passenger_count)

response = requests.get(url, params=params)

prediction = response.json()
if (data.lat[0] <= 40) or (data.lat[0] >=42) or (data.lon[0] <= -74.3) or (data.lon[0] >=-72.9):
    st.sidebar.warning("Your pickup location is out of range")
elif (data.lat[1] <= 40) or (data.lat[1] >=42) or (data.lon[1] <= -74.3) or (data.lon[1] >=-72.9):
    st.sidebar.warning("Your pickup location is out of range")
else:
    st.success(f'The estimated Fare will be {round(prediction["fare_amount"],2)} $')
