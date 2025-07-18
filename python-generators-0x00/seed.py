import mysql.connector
import csv
import uuid
from mysql.connector import errorcode

DB_NAME = 'ALX_prodev'

def connect_db():
    """Connects to MySQL server (without specifying a database)"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it does not exist"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created or already exists")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects directly to the ALX_prodev database"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='your_mysql_user',
            password='your_mysql_password',
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Creates the user_data table if it does not exist"""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    );
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_sql)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, csv_file):
    """Reads data from CSV and inserts it into the table if not already present"""
    cursor = connection.cursor()
    inserted_count = 0
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                uid = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                # Check if email already exists to prevent duplicate inserts
                cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (uid, name, email, age))
                inserted_count += 1

        connection.commit()
        print(f"{inserted_count} records inserted.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
