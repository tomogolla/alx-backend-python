
````markdown
# ALX ProDev — MySQL Seeder

This project automates the setup and population of a MySQL database (`alx_prodev`) with sample user data using a Python script. It demonstrates database connection, creation, table management, CSV ingestion, and row-by-row data streaming with generators.

---

## Features

- Connects to a MySQL server instance
- Creates a database `alx_prodev` if it doesn’t exist
- Creates a `user_data` table with appropriate schema
- Reads and inserts records from a CSV file (`user_data.csv`)
- Prevents duplicate inserts using `INSERT IGNORE`
- Streams database rows using a Python generator function

---

## Database Schema — `user_data`

| Column     | Type         | Details                        |
|------------|--------------|--------------------------------|
| `user_id`  | `CHAR(36)`   | Primary Key, UUID, Indexed     |
| `name`     | `VARCHAR`    | Not Null                       |
| `email`    | `VARCHAR`    | Not Null                       |
| `age`      | `DECIMAL`    | Not Null                       |

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/alx-mysql-seeder.git
cd alx-mysql-seeder
````

### 2. Set Up Python Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies

```bash
pip install mysql-connector-python pandas
```

> You can optionally create a `requirements.txt` for this.

---

## Configuration

In `seed.py`, update your MySQL credentials:

```python
user='root',
password='your_password',
host='localhost'
```

Ensure your MySQL server is running locally before executing the script.

---

## Sample CSV Format — `user_data.csv`

```csv
user_id,name,email,age
c1f0e9c2-1a45-11ee-be56-0242ac120002,Jane Doe,jane@example.com,28
b0d2f3a4-7e90-4fc0-9f3f-bcbcedbfeaef,John Smith,john@example.com,34
```

Place the file in the same directory as `seed.py`.

---

## Running the Seeder Script

```bash
python seed.py
```

Expected output:

```
Database alx_prodev ensured.
Table user_data ensured.
Inserted 2 rows into user_data.
```

---

## Streaming with a Generator

The script includes a generator function `stream_user_data()` that yields one row at a time from the table:

```python
for user in stream_user_data():
    print(user)
```

Useful for memory-efficient batch processing and analytics.
---

## Contribution

Pull requests and issue reports are welcome. Feel free to fork and improve the project.

```

