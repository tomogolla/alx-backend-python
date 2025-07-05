#!/usr/bin/python3
import seed

def stream_user_ages():
    """
    Generator that yields one user age at a time from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    
    while True:
        row = cursor.fetchone()
        if not row:
            break
        yield row[0]

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes the average age using the generator stream_user_ages.
    No more than 2 loops. No use of SQL AVG.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 1
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    compute_average_age()
