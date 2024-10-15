import requests
import streamlit as st
import time

def get_weather(lat, lon):
    api_key = "a8515bde5d684070b32150756242709"  # Your WeatherAPI key
    base_url = "http://api.weatherapi.com/v1/current.json"  # WeatherAPI URL for current weather data
    
    # Set parameters: latitude and longitude combined as 'q', and API key
    params = {
        'key': api_key,
        'q': f"{lat},{lon}",  # Query is latitude and longitude combined
        'aqi': 'no'  # Disable air quality index in response
    }
    
    # Get the response from the WeatherAPI
    response = requests.get(base_url, params=params)
    
    # Check if the status code is 200 (OK)
    if response.status_code == 200:
        try:
            # Convert response data to JSON format
            data = response.json()
            
            if "current" in data:
                current = data["current"]
                temperature = current["temp_c"]  # Temperature in Celsius
                weather_desc = current["condition"]["text"]
                humidity = current["humidity"]
                pressure = current["pressure_mb"]

                return {
                    'Temperature': f"{temperature}°C",
                    'Weather': weather_desc,
                    'Humidity': f"{humidity}%",
                    'Pressure': f"{pressure} hPa"
                }
            else:
                return {"Error": "Weather data not found."}
        except requests.exceptions.JSONDecodeError:
            return {"Error": "Failed to parse JSON response."}
    else:
        return {"Error": f"Unable to fetch data. Status code {response.status_code}"}

if __name__ == "__main__":
    st.title("Weather Information")

    # Latitude and Longitude Input from user
    lat = st.text_input("Enter Latitude", "26.922070")  # Default is for Jaipur
    lon = st.text_input("Enter Longitude", "75.778885")

    if st.button("Get Weather") or True:  # Always load weather on app start
        while True:
            weather_data = get_weather(lat, lon)

            if "Error" in weather_data:
                st.error(weather_data["Error"])
            else:
                # Display the weather data
                st.write(f"**Temperature**: {weather_data['Temperature']}")
                st.write(f"**Weather**: {weather_data['Weather']}")
                st.write(f"**Humidity**: {weather_data['Humidity']}")
                st.write(f"**Pressure**: {weather_data['Pressure']}")

            # Refresh the data every 5 minutes (300 seconds)
            time.sleep(300)
            st.experimental_rerun()  # Rerun the script to refresh the data
