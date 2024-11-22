import streamlit as st
import requests
from datetime import datetime
import folium
from streamlit_folium import folium_static

# Title
'''
# Taxi Fare Prediction
'''

# Collecting inputs
st.markdown('''
## Enter the ride details:
''')

pickup_datetime = st.text_input('Pickup Date & Time (YYYY-MM-DD HH:MM:SS):', value=str(datetime.now()))
pickup_longitude = st.number_input('Pickup Longitude:', value=-73.985428)
pickup_latitude = st.number_input('Pickup Latitude:', value=40.748817)
dropoff_longitude = st.number_input('Dropoff Longitude:', value=-73.985428)
dropoff_latitude = st.number_input('Dropoff Latitude:', value=40.748817)
passenger_count = st.number_input('Number of Passengers:', min_value=1, max_value=6, value=1)

# API URL
api_url = 'https://taxifare.lewagon.ai/predict'  # Replace with your own API URL if available

# Prediction button
if st.button('Predict Fare'):
    # Prepare the parameters for the API request
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count,
    }

    try:
        # API request
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Ensure the request was successful

        # Parse the response
        result = response.json()
        fare_prediction = result.get('fare', 'Prediction not available')

        # Display the result
        st.markdown(f"## Predicted Fare: ${fare_prediction:.2f}")

        # Define map data
        # Define the map
        m = folium.Map(location=[(pickup_latitude + dropoff_latitude) / 2,
                                (pickup_longitude + dropoff_longitude) / 2], zoom_start=12)

        # Add markers
        folium.Marker([pickup_latitude, pickup_longitude], tooltip="Pickup").add_to(m)
        folium.Marker([dropoff_latitude, dropoff_longitude], tooltip="Dropoff").add_to(m)

        # Render the map in Streamlit
        folium_static(m)

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
    except ValueError:
        st.error("Invalid response received from the API.")
