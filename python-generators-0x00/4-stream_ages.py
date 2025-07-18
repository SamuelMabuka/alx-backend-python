import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one from the user_data table"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password',
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  # yields each age tuple unpacked
            yield age

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def compute_average_age():
    """Computes and prints the average age using the generator"""
    total = 0
    count = 0

    for age in stream_user_ages():  # loop 1
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No user data found.")