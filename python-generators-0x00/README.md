# Seeder

This project sets up a MySQL database named `ALX_prodev`, creates a table called `user_data`, and populates it with user records from a CSV file.

## Features

- Creates the `ALX_prodev` database if it doesn't exist.
- Creates a `user_data` table with:
  - `user_id` (UUID, Primary Key)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Prevents duplicate entries based on email.
- Populates the table using data from a `user_data.csv` file.

---

## File Structure

```bash
.
├── 0-main.py         # Entry point that calls functions in seed.py
├── seed.py           # Contains all logic to setup DB, table, and insert data
├── user_data.csv     # Sample CSV data to populate the database
└── README.md         # Project documentation
