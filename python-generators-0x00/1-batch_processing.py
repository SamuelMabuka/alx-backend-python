import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields user_data rows in batches"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password',
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def batch_processing(batch_size):
    """Returns a list of users over age 25"""
    filtered_users = []

    for batch in stream_users_in_batches(batch_size):       # Loop 1
        for user in batch:                                  # Loop 2
            if user['age'] > 25:
                filtered_users.append(user)

    return filtered_users