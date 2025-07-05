
```markdown
# MySQL User Data Seeder

This project sets up and populates a MySQL database (`alx_prodev`) with sample user data from a CSV file using Python.

## Project Structure

```

.
├── seed.py               # Main script to create DB, table, and insert data
├── user\_data.csv         # CSV file containing sample user data
├── requirements.txt      # Python dependencies (optional)
└── README.md             # Project documentation

````

---

## Features

- Automatically connects to MySQL server
- Creates database `alx_prodev` if it doesn’t exist
- Creates a `user_data` table with required fields
- Loads and inserts data from `user_data.csv`
- Avoids inserting duplicates
- Includes a generator function to stream rows one-by-one

---

## Table Schema: `user_data`

| Field     | Type       | Description                     |
|-----------|------------|---------------------------------|
| user_id   | UUID (PK)  | Unique identifier for each user |
| name      | VARCHAR    | User's full name                |
| email     | VARCHAR    | User's email address            |
| age       | DECIMAL    | User's age                      |

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
````

### 2. Set Up Environment

#### Option A: Using Conda

```bash
conda create -n alx-env python=3.11
conda activate alx-env
pip install -r requirements.txt
```

#### Option B: Using `venv`

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Install Dependencies

```bash
pip install mysql-connector-python pandas
```

### 4. Configure MySQL

Ensure MySQL is running locally, and your credentials in `seed.py` are correct:

```python
user='root'
password='admin@123'
host='localhost'
```

### 5. Run the Script

```bash
python seed.py
```

---
##  Generator Function

The script includes a generator `stream_user_data()` that streams rows from the `user_data` table one at a time.

Example:

```python
for row in stream_user_data():
    print(row)
```

---

## Sample CSV Format (`user_data.csv`)

```csv
user_id,name,email,age
a1b2c3d4-5678-9101-1121-314151617181,Jane Doe,jane@example.com,28
b2c3d4e5-6789-1011-1213-415161718192,John Smith,john@example.com,34
```
---

## Contributing

Feel free to fork the repo and submit pull requests to improve functionality or documentation.

```

---


