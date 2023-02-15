from datetime import datetime
import requests
import config
import main

API_KEY = config.API_KEY


def current_weather_search(coordinates):
    """
    Makes a call to the OpenweatherMap API
    for current weather data in a specifed location.
    Prints the data to the terminal.
    """

    lat = coordinates[0]
    lon = coordinates[1]
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}"
        f"&exclude=minutely,hourly,daily&units=metric&appid={API_KEY}")
    res = requests.get(url, timeout=60)
    data = res.json()

    temperature = data["current"]["temp"]
    wind_speed = data["current"]["wind_speed"]
    humidity = data["current"]["humidity"]
    pressure = data["current"]["pressure"]
    summary = data['current']['weather'][0]['main']
    description = data['current']['weather'][0]['description']
    print(f"""
    Temperature-- {temperature} °C
    Summary -- {summary}
    Description -- {description}
    Wind Speed -- {wind_speed} m/s
    Humidity -- {humidity} %
    Pressure -- {pressure} hPa
    """)


def geocode_location(location, country_code):
    """
    Converts Location by name and Country code to
    Latitude and Longitude Coordinates for use in
    Weather API calls
    """
    try:
        url = (
            f"http://api.openweathermap.org/geo/1.0/direct?q={location},"
            f"{country_code}&limit=1&appid={API_KEY}")

        res = requests.get(url, timeout=60)
        data = res.json()

        if len(data) > 0:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            coordinates = (lat, lon)
            return coordinates
        else:
            print("Unable to Find Location, Please Try Again")
            main.display_menu()

    except requests.exceptions.HTTPError as ex:
        print("An error occurred while making the API request:", ex)
        main.display_menu()


def hourly_interval_forecast(coordinates):
    """
    Calls to the OpenWeather Map API and
    Displays, weather forecast in hourly intervals.
    Displays it for 12 hours ahead in the desired
    location from user input
    """

    try:
        lat = coordinates[0]
        lon = coordinates[1]
        url = (
            f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}"
            f"&lon={lon}&exclude=minutely,daily,current&units=metric"
            f"&appid={API_KEY}")

        res = requests.get(url, timeout=60)
        res.raise_for_status()

    except requests.exceptions.Timeout:
        print("Connection to OpenWeatherMap API timed out.")
        print("Please try again")

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        print("Please Try Again")

    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        print("Please Try again")

    data = res.json()

    hourly_data = data["hourly"][0:12]

    for hourly in hourly_data:
        timestamp = datetime.fromtimestamp(hourly["dt"])
        temperature = hourly["temp"]
        description = hourly["weather"][0]["description"]
        wind_speed = hourly["wind_speed"]
        humidity = hourly["humidity"]
        pressure = hourly["pressure"]
        description = description.title()

        print(f"""
            {timestamp.strftime('%H:%M')}:
            {description},
            Temperature -- {temperature} °C
            Wind Speed -- {wind_speed} m/s
            Humidity -- {humidity} %
            Pressure -- {pressure} hPa
            """)


def five_day_forecast(coordinates):
    """
    Calls to the Openweather Map API and
    Displays a 5 day weather forecast for
    the specified location.
    """
    try:
        lat = coordinates[0]
        lon = coordinates[1]

        url = (
            f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}"
            f"&lon={lon}&exclude=minutely,hourly,current&units=metric"
            f"&appid={API_KEY}")

        res = requests.get(url, timeout=60)
    except requests.exceptions.Timeout:
        print("Connection to OpenWeatherMap API timed out.")
        print("Please try again")

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        print("Please Try Again")

    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        print("Please Try again")
       
    data = res.json()

    daily_data = data["daily"][0:5]

    for day in daily_data:
        timestamp = datetime.fromtimestamp(day["dt"])
        morning_temp = day["temp"]["morn"]
        day_temp = day["temp"]["day"]
        night_temp = day["temp"]["night"]
        eve_temp = day["temp"]["eve"]
        description = day["weather"][0]["description"]
        wind_speed = day["wind_speed"]
        humidity = day["humidity"]
        pressure = day["pressure"]
        description = description.title()

        print(f"""
            {timestamp.strftime('%A')}:
            {description},
            Temperature:
                Morning -- {morning_temp} °C
                Day -- {day_temp} °C
                Evening -- {eve_temp} °C
                Night -- {night_temp} °C
            Wind Speed -- {wind_speed} m/s
            Humidity -- {humidity} %
            Pressure -- {pressure} hPa
            """)
