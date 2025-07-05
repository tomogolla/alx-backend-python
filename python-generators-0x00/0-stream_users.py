import mysql.connector

def stream_users():
    """
    Generator that streams user records one at a time from the user_data table.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin@123',  
            database='alx_prodev'
        )
        cursor = conn.cursor()s
        cursor.execute("SELECT * FROM user_data")

        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row

    except mysql.connector.Error as err:
        print("Database error:", err)

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
