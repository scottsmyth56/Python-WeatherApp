import weather
import db


def display_menu():
    """
    Inital Startu menu displayed to user. Giving user
    choices based on what actions they wish to perform
    """
    print(
        """
    *Welcome to PyWeather*\n
    Registered Users can avail of more features such as
    - Favourite Locations
    - 5 Day Forecast
    Choose an option to get started

    1. Login
    2. Register
    3. Current Weather Forecast
    4. Hourly Interval Forecast
    5. Exit Program

    """
    )
    validate_choice()


def validate_choice():
    """
    Checks the user choice for valid input
    Calls the requested action based on user choice
    """
    try:
        choice = int(input("Enter Choice:\n"))
        if choice not in [1, 2, 3, 4, 5]:
            raise ValueError
    except ValueError:
        print("\nError: Input must be a number between 1-3,please try again")
        display_menu()

    if choice == 1:
        db.login()
    elif choice == 2:
        db.register_user()
    elif choice == 3:
        display_current_weather()
    elif choice == 4:
        location = enter_location()
        coordinates = weather.geocode_location(location[0], location[1])
        print(f"Finding Hourly forecast for {location[0]}...")
        weather.hourly_interval_forecast(coordinates)
        get_user_action(False, "")
    elif choice == 5:
        print("Exiting Program..")
        exit()


def get_user_action(logged_in, username):

    """
    Recieves user input and determines there
    next action based on the input and if the
    user is logged in or not making the
    proper method call for requested action/
    """
    if logged_in is False:
        print(
            """
            Choose an action from the menu
            1.Return to Main Menu
            2.Search weather again
            3.Exit Program
            """
        )

        try:
            choice = int(input("Enter Choice:\n"))
            if choice not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print(
                "\nError: Choice must be either 1 or 2 and"
                + "not a character, please try again"
            )
            display_menu()

        if choice == 1:
            display_menu()
        elif choice == 2:
            location = enter_location()
            coordinates = weather.geocode_location(location[0], location[1])
            weather.hourly_interval_forecast(coordinates)
            get_user_action(False, "")
        elif choice == 3:
            print("Exiting Program")
            exit()
    else:
        print(
            """
            Choose an action from the menu
            1.Return to Home Menu
            2.Search 5 Day Forecast
            3.Search Hourly Interval Forecast.
            4. Exit Program
            """
        )

        try:
            choice = int(input("Enter Choice:\n"))
            if choice not in [1, 2, 3, 4]:
                raise ValueError
        except ValueError:
            print(
                "\nError: Choice must be either 1, 2 or 3 and"
                + "not a character, please try again"
            )
            get_user_action(True, username)

        if choice == 1:
            display_user_home_menu(username)
        elif choice == 2:
            location = enter_location()
            coordinates = weather.geocode_location(location[0], location[1])
            weather.five_day_forecast(coordinates)
            get_user_action(True, username)
        elif choice == 3:
            location = enter_location()
            coordinates = weather.geocode_location(location[0], location[1])
            weather.hourly_interval_forecast(coordinates)
            get_user_action(True, username)
        elif choice == 4:
            print("Exiting Program..")
            exit()


def display_user_home_menu(username):

    """
    Displays logged in users home menu with
    choices to add new favourite locations,Search
    weather in favourite locations, view locations and
    General weather Search in any desired location
    """
    print(f"Welcome Back {username}")
    print(
        """
    \nChoose an option from the menu:
    1. Add Favourite Location.
    2. Search Weather in Favourite Locations.
    3. Current Weather Data with hourly interval.
    4. 5 Day Forecast.
    5. Change Password.
    6. Logout.
    7. Exit Program

    """
    )

    try:
        choice = int(input("Enter Choice:\n"))
        if choice not in [1, 2, 3, 4, 5, 6, 7]:
            raise ValueError
    except ValueError:
        print("\nError: Input must be a number between 1-4,please try again")
        display_user_home_menu(username)

    if choice == 1:
        db.add_favourite_location(username)
        get_user_action(True, username)
    elif choice == 2:
        db.view_favourite_location_weather(username)
        get_user_action(True, username)
    elif choice == 3:
        location = enter_location()
        coordinates = weather.geocode_location(location[0], location[1])
        print(f"Finding Hourly forecast for {location[0]}")
        weather.hourly_interval_forecast(coordinates)
        get_user_action(True, username)
    elif choice == 4:
        location = enter_location()
        coordinates = weather.geocode_location(location[0], location[1])
        print(f"Finding 5 day forecast for {location[0]}")
        weather.five_day_forecast(coordinates)
        get_user_action(True, username)
    elif choice == 5:
        db.user_change_password(username)
    elif choice == 6:
        print("Logging out..")
        display_menu()
    elif choice == 7:
        print("Exiting Program..")
        exit()


def enter_location():
    """
    Takes the location name and country
    from the user and returns them as a tuple
    """

    location = input("Enter a Location:\n")
    if len(location) == 0:
        print("Location cannot be empty,Please Try again")
        enter_location()
    country = input(
        """
        Enter the country your location is in.
        For more accurate results enter the country code e.g IE = Ireland.
        Enter Country:\n""")
    if len(country) == 0:
        print("Country cannot be empty,Please Try again")
        enter_location()

    location_tuple = (location, country)
    return location_tuple


def display_current_weather():
    """
    Displays live weather data for any location
    the user inputs if the input data is valid
    """

    location = enter_location()
    coordinates = weather.geocode_location(location[0], location[1])
    print(f"Finding Current Weather in {location[0]}, {location[1]}")
    weather.current_weather_search(coordinates)
    get_user_action(False, "")


def run():
    """
    Starts the program run by loading start menu
    """
    display_menu()
