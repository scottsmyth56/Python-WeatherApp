import os
from datetime import datetime
import requests
import mysql.connector
from dotenv import load_dotenv


load_dotenv()

USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")
HOST = os.environ.get("DB_HOST")
NAME = os.environ.get("DB_NAME")
API_KEY = os.environ.get("API_KEY")

conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    port=PORT,
    database=NAME
    )

cursor = conn.cursor()


def display_menu():
    """
    Inital Startu menu displayed to user. Giving user
    choices based on what actions they wish to perform
    """
    print("""
    *Welcome to Python Weather App*
    Choose an option to get started

    1. Login
    2. Register
    3. Curent Weather Forecast

    """)
    validate_choice()


def validate_choice():
    """
    Checks the user choice for valid input
    Calls the requested action based on user choice
    """
    try:
        choice = int(input("Enter Choice:"))
        if choice not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        print("\nError: Input must be a number between 1-3,please try again")
        display_menu()

    if choice == 1:
        login()
    elif choice == 2:
        register_user()
    elif choice == 3:
        display_current_weather()


def login():
    """
     Checks for existing user in database, if user is
     found, the user enters password and logs in.
     If the user doesn't exist error message is displayed
     prompting the user to try again or register.
    """

    username = input("Enter your username: ")
    cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        input_password = input("Enter your password: ")
        print("Checking Credentials..")
        cursor.execute(
            "SELECT PASSWORD FROM User WHERE username = %s", (username,))
        user_password = cursor.fetchone()
        if input_password == user_password[0]:
            print("Login SuccessFul")
            display_user_home_menu(username)
        else:
            print("Incorrect password, please try again")
            login()
    else:
        print("Username not found. Please try again or register.")
        display_menu()


def register_user():
    """
     Registers new user on the system with username and password
    If user already exists, messages is displayed,
    If user doesn't exist, the user is registered on the system
    """

    username = input(("Enter a username: "))
    cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        print("User already Exists Please Try a Different Username")
        register_user()
    else:
        password = input("Enter a password: ")
        cursor.execute(
            "INSERT INTO User (username, password) VALUES (%s, %s)",
            (username, password))
        conn.commit()
        print(f"{username} registered succesfully")
        display_user_home_menu(username)


def display_current_weather():
    """
    Displays live weather data for any location
    the user inputs if the input data is valid
    """

    location = input("Enter a Location: ")
    country = input("""
    *Enter the country your location is in.
    For more accurate results enter the country code e.g IE = Ireland.*
    Enter country: """)
    coordinates = geocode_location(location, country)
    print(f"Finding Current Weather in {location}, {country}")
    current_weather_search(coordinates)


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
            print("Unable to convert coordinates, Please Try Again")
            display_menu()

    except requests.exceptions.HTTPError as ex:
        print("An error occurred while making the API request:", ex)
        display_menu()


def display_user_home_menu(username):

    """
     Displays logged in users home menu with
     choices to add new favourite locations,Search
     weather in favourite locations, view locations and
     General weather Search in any desired location
    """
    print(f"Welcome Back {username}")
    print("""
    \nChoose an option from the menu:
    1. Add Favourite Location.
    2. Search Weather in Favourite Locations.
    3. Current Weather Data with hourly interval.
    4. 5 Day Forecast.
    5. Change Password.

    """)

    try:
        choice = int(input("Enter Choice:"))
        if choice not in [1, 2, 3, 4]:
            raise ValueError
    except ValueError:
        print("\nError: Input must be a number between 1-4,please try again")
        display_menu()

    if choice == 1:
        add_favourite_location(username)
    elif choice == 2:
        view_favourite_location_weather(username)
    elif choice == 3:
        # current_weather_hour_interval(username)
        print("gg")
    elif choice == 4:
        print("Add method call")  # quick_search()


def main():
    """
    Program run function
    """
    display_menu()


def add_favourite_location(username):
    """
    Allows logged in users to save favourite locations
    so they can easily search the weather forecast in those
    locations instead of searching again
    """
    print("""
    Enter Location and the  Location Country  to save as favourite location.
    For Better Results add the Country Code instead of Full Country Name.
    e.g ( IE = Ireland)
    """)

    location = input("Enter Location: ")
    country = input("Enter Country or Country Code: ")
    try:
        coordinates = geocode_location(location, country)
        lat = coordinates[0]
        lon = coordinates[1]

    except Exception as ex:
        print("Error while recieving coordinates", ex)

    try:
        cursor.execute(
                "INSERT INTO Locations (username, location, Lat, Lon)" +
                "VALUES (%s, %s, %s, %s)",
                (username, location, lat, lon))
        conn.commit()
        print(f"{location} in {country} was added to favourites succesfully")

    except mysql.connector.Error as ex:
        print("Error while saving location", ex)
    display_user_home_menu(username)


def view_favourite_location_weather(username):
    """
    Allows logged in users to quickly view the weather in
    favourite locations wihtout having to manual search again.
    """
    cursor.execute(
        "SELECT Location, Lat, Lon FROM Locations" +
        " WHERE username = %s", (username,))
    fav_locations = cursor.fetchall()

    if len(fav_locations) <= 0:
        print("""
        You have no saved locations.
        Please add favourite locations to use this quick search feature""")
        display_user_home_menu(username)
    else:
        print("Select a location:")
        for i, loc in enumerate(fav_locations):
            print(f"{i+1}. {loc[0]}")

        selected_index = int(input(
            "Enter the number of the location" +
            " you want to see the weather for: ")) - 1
        selected_location = fav_locations[selected_index]
        coordinates = (selected_location[1], selected_location[2])

        try:
            choice = int(input("""
                *Choose Your Desired Forecast*
                1. Hourly Forecast for 12 Hours.
                2. 5 Day Forecast.
            """))

            if choice not in [1, 2]:
                raise ValueError

        except ValueError:
            print("\nError: Your Choice must be either 1 or 2 and not a character,please try again")
            view_favourite_location_weather(username)

        if choice == 1:
            print(f"Finding Hourly Forecast for: {selected_location[0]} ")
            hourly_interval_forecast(coordinates)
        elif choice == 2:
            print(f"Finding 5 Day Forecast for: {selected_location[0]} ")
            five_day_forecast(coordinates)


def hourly_interval_forecast(coordinates):
    """
    Calls to the OpenWeather Map API and
    Displays, weather forecast in hourly intervals.
    Displays it for 12 hours ahead in the desired
    location from user input
    """

    lat = coordinates[0]
    lon = coordinates[1]
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}"
        f"&lon={lon}&exclude=minutely,daily,current&units=metric"
        f"&appid={API_KEY}")

    res = requests.get(url, timeout=60)
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
    lat = coordinates[0]
    lon = coordinates[1]

    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}"
        f"&lon={lon}&exclude=minutely,hourly,current&units=metric"
        f"&appid={API_KEY}")

    res = requests.get(url, timeout=60)
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


main()
