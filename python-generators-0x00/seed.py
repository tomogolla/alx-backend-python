import mysql.connector
import pandas as pd
from mysql.connector import errorcode

# 1. Connect to MySQL Server (no DB yet)
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin@123'  
        )
        return conn
    except mysql.connector.Error as err:
        print("Error:", err)
        return None

# 2. Create ALX_prodev database if it doesn't exist
def create_database(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev ensured.")
    except mysql.connector.Error as err:
        print("Failed creating database:", err)
    cursor.close()

# 3. Connect directly to ALX_prodev
def connect_to_prodev():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',   
            database='ALX_prodev'
        )
        return conn
    except mysql.connector.Error as err:
        print("Error:", err)
        return None

# 4. Create user_data table
def create_table(conn):
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data ensured.")
    except mysql.connector.Error as err:
        print("Failed creating table:", err)
    cursor.close()

# 5. Insert user data from CSV (skip existing)
def insert_data(conn, data):
    cursor = conn.cursor()
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Inserted {cursor.rowcount} rows into user_data.")
    except mysql.connector.Error as err:
        print("Insert error:", err)
    cursor.close()

# Utility to read CSV
def load_csv(filepath):
    df = pd.read_csv(filepath)
    return [tuple(row) for row in df.values]

# 🏁 Main runner
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)
        user_data = load_csv("csv-data/user_data.csv")
        insert_data(db_conn, user_data)
        db_conn.close()

def stream_users():
    conn = connect_to_prodev()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
    conn.close()

# Usage
for user in stream_users():
    print(user)
