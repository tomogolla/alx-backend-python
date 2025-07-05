import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields rows from user_data in batches of batch_size.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin@123', 
            database='alx_prodev'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_data")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows

    except mysql.connector.Error as err:
        print("Database error:", err)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def batch_processing(batch_size):
    """
    Processes batches of users, yielding only users older than 25.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        filtered = [user for user in batch if user[3] > 25]  # Loop 2 (list comprehension)
        yield filtered  # Generator does not count as a loop

