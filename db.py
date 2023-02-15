import mysql.connector
import weather
import config
import main


conn = mysql.connector.connect(
    host=config.HOST,
    user=config.USER,
    password=config.PASSWORD,
    port=config.PORT,
    database=config.NAME,
)

cursor = conn.cursor()


def login():
    """
    Checks for existing user in database, if user is
    found, the user enters password and logs in.
    If the user doesn't exist error message is displayed
    prompting the user to try again or register.
    """

    username = input("Enter your username:\n")
    cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        input_password = input("Enter your password:\n")
        print("Checking Credentials..")
        cursor.execute(
            "SELECT PASSWORD FROM User"
            " WHERE username = %s", (username,))
        user_password = cursor.fetchone()
        if input_password == user_password[0]:
            print("Login Successfull")
            main.display_user_home_menu(username)
        else:
            print("Incorrect password, please try again")
            login()
    else:
        print("Username not found. Please try again or register.")
        main.display_menu()


def register_user():
    """
     Registers new user on the system with username and password
    If user already exists, messages is displayed,
    If user doesn't exist, the user is registered on the system
    """

    username = input(("Enter a username:\n"))
    cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        print("User already Exists Please Try a Different Username")
        register_user()
    else:
        password = input("Enter a password:\n")
        cursor.execute(
            "INSERT INTO User (username, password) VALUES (%s, %s)",
            (username, password),
        )
        conn.commit()
        print(f"{username} registered succesfully")
        main.display_user_home_menu(username)


def add_favourite_location(username):
    """
    Allows logged in users to save favourite locations
    so they can easily search the weather forecast in those
    locations instead of searching again
    """
    print(
        """
    Enter Location and the  Location Country  to save as favourite location.
    For Better Results add the Country Code instead of Full Country Name.
    e.g ( IE = Ireland)
    """
    )

    location = input("Enter Location:\n")
    country = input("Enter Country or Country Code:\n")
    try:
        coordinates = weather.geocode_location(location, country)
        lat = coordinates[0]
        lon = coordinates[1]

    except IndexError() as ex:
        print("Error while recieving coordinates", ex)

    try:
        cursor.execute(
            "INSERT INTO Locations (username, location, Lat, Lon)"
            + "VALUES (%s, %s, %s, %s)",
            (username, location, lat, lon),
        )
        conn.commit()
        print(f"{location} in {country} was added to favourites succesfully")

    except mysql.connector.Error as ex:
        print("Error while saving location", ex)
    main.display_user_home_menu(username)


def view_favourite_location_weather(username):
    """
    Allows logged in users to quickly view the weather in
    favourite locations wihtout having to manual search again.
    """
    cursor.execute(
        "SELECT Location, Lat, Lon FROM Locations" +
        " WHERE username = %s", (username,)
    )
    fav_locations = cursor.fetchall()

    if len(fav_locations) <= 0:
        print(
            """
        You have no saved locations.
        Please add favourite locations to use this quick search feature"""
        )
        main.display_user_home_menu(username)
    else:
        print("Select a location:")
        for i, loc in enumerate(fav_locations):
            print(f"{i+1}. {loc[0]}")

        selected_index = (
            int(input(
                    "Enter the number of the location"
                    + " you want to see the weather for:\n"
                )) - 1
        )
        selected_location = fav_locations[selected_index]
        coordinates = (selected_location[1], selected_location[2])

        try:
            choice = int(input(
                """
                *Choose Your Desired Forecast*
                1. Hourly Forecast for 12 Hours.
                2. 5 Day Forecast.\n"""
                ))

            if choice not in [1, 2]:
                raise ValueError

        except ValueError:
            print(
                "\nError: Your Choice must be either"
                + "1 or 2 and not a character,please try again"
            )
            view_favourite_location_weather(username)

        if choice == 1:
            print(f"Finding Hourly Forecast for: {selected_location[0]} ")
            weather.hourly_interval_forecast(coordinates)
        elif choice == 2:
            print(f"Finding 5 Day Forecast for: {selected_location[0]} ")
            weather.five_day_forecast(coordinates)


def user_change_password(username):
    """
    Allows the user to change their login password,
    User's must confirm their current password to change
    to a new password.
    """
    current_password_input = input("Enter Current Password:\n")

    cursor.execute(
        "SELECT Password FROM User"
        " WHERE username = %s", (username,))
    current_password = cursor.fetchone()

    if current_password[0] == current_password_input:
        new_password = input("Enter new password:\n")
        new_password_confirm = input("Confirm new password:\n")
        if new_password == new_password_confirm:
            cursor.execute(
                f"UPDATE User SET password = {new_password}"
                f" WHERE username = {username}; "
            )
            conn.commit()
            print("\nPassword Changed")
            main.display_user_home_menu(username)
        else:
            print("Passwords do not match, Please Try again")
            user_change_password(username)
    else:
        print("Incorrect Password, Please Try again")
        user_change_password(username)
