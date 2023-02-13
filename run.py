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


def displayMenu():

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

    try:
        choice = input("Enter Choice:")
        choice = int(choice)
        if choice not in [1, 2, 3]:
            raise ValueError
            # displayMenu()
        return choice
    except ValueError:
        print("\nError: Input must be a number between 1-3,please try again")
        displayMenu()




# def _main_():
displayMenu()


