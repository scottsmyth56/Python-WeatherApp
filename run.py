import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASSWORD")
PORT = os.environ.get("DB_PORT")
HOST = os.environ.get("DB_HOST")
NAME = os.environ.get("DB_NAME")

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
    3. Quick search for Forecast

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
        quick_search()


def login():
    print("Test login call")


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
        cursor.execute("INSERT INTO User (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        print(f"{username} registered succesfully")


def quick_search():
    print("test quick search call")


def _main_():
    display_menu()


_main_()
