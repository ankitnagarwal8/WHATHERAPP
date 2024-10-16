import requests
import streamlit as st
from datetime import datetime
import pytz

# Define the IST timezone
ist = pytz.timezone('Asia/Kolkata')

# Function to get location details using apiip.net API, with default fallback to New Delhi, India
def get_location():
    try:
        # API URL with access key and predefined IP address
        api_key = "c0fc6f0e-7ca6-49ac-b588-347c2776a51a"
        api_url = f"https://apiip.net/api/check?accessKey={api_key}"
        
        # Get the location data from the API
        response = requests.get(api_url)
        data = response.json()
        
        if response.status_code == 200:
            # Extract location details from API response
            latitude = data.get('location', {}).get('latitude', '28.6139')  # Fallback to New Delhi if missing
            longitude = data.get('location', {}).get('longitude', '77.2090')  # Fallback to New Delhi if missing
            city = data.get('city', 'New Delhi')  # Fallback to New Delhi if city is not found
            
            return latitude, longitude, city
        else:
            # If API call fails, fallback to New Delhi
            return "28.6139", "77.2090", "New Delhi"
    except Exception as e:
        # Default to New Delhi, India if an error occurs
        return "28.6139", "77.2090", "New Delhi"

# Function to get weather information based on latitude and longitude
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

# CSS for simple animations and colored text
st.markdown("""
    <style>
        .city-name {
            font-size: 32px;
            font-weight: bold;
            color: #FF5733; /* Reddish-orange for location */
            animation: glow 1.5s infinite;
        }

        .temperature {
            font-size: 28px;
            font-weight: bold;
            color: #33FF57; /* Green for temperature */
        }

        .weather-condition {
            font-size: 26px;
            font-weight: bold;
            color: #3380FF; /* Blue for weather description */
            animation: float 2s infinite ease-in-out;
        }

        .humidity {
            font-size: 24px;
            color: #FF33FF; /* Pinkish color for humidity */
        }

        .pressure {
            font-size: 24px;
            color: #FFAC33; /* Orange for pressure */
        }

        /* Animation for glowing effect on the city name */
        @keyframes glow {
            0% { text-shadow: 0 0 5px #FF5733, 0 0 10px #FF5733; }
            50% { text-shadow: 0 0 20px #FF5733, 0 0 30px #FF5733; }
            100% { text-shadow: 0 0 5px #FF5733, 0 0 10px #FF5733; }
        }

        /* Floating animation for weather description */
        @keyframes float {
            0% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    st.title("🌦️ Animated Weather Dashboard")

    # Automatically get the user's location and city name
    lat, lon, city = get_location()

    # Get the current time in IST
    current_time_ist = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S %Z')

    st.markdown(f"**Current IST Time:** {current_time_ist}")  # Display the IST time

    if lat and lon and city:
        st.markdown(f"<div class='city-name'>📍 {city}</div>", unsafe_allow_html=True)
        
        # Fetch the weather data
        weather_data = get_weather(lat, lon)
        
        if "Error" in weather_data:
            st.error(weather_data["Error"])
        else:
            # Display the weather data with different colors and simple animations
            st.markdown(f"<div class='temperature'>🌡️ Temperature: {weather_data['Temperature']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='weather-condition'>☁️ Weather: {weather_data['Weather']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='humidity'>💧 Humidity: {weather_data['Humidity']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='pressure'>🔽 Pressure: {weather_data['Pressure']}</div>", unsafe_allow_html=True)
    else:
        st.error("Unable to retrieve location data. Please try again.")
