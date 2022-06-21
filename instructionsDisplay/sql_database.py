import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error is: {e}")
    finally:
        if connection:
            connection.close()
            print("Connection closed")

    return connection
