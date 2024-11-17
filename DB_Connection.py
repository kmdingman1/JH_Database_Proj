import mysql.connector
from mysql.connector import Error


def connect_to_database():
    try:
        # Establish a connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='COSC578_Hopkins',
            database='hopkins_health_hub'
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            # Return the connection object to use it elsewhere
            return connection

    except Error as e:
        print(f"Error: '{e}' occurred")
        return None

    return None


# Test the connection
db_connection = connect_to_database()
if db_connection:
    db_connection.close()
