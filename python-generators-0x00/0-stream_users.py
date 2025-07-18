import mysql.connector

def stream_users():
    """Generator that yields one row at a time from the user_data table"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password',
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
