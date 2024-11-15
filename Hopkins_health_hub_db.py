import pymysql

def connect_to_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='COSC578_Hopkins',
            database='hopkins_health_hub_db',
            port=3306
        )
        print("Successfully connected to the database!")
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        conn.close()