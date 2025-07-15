import sqlite3

# ✅ Class-based context manager
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        print("[INFO] Database connection opened.")
        return self.conn  # this will be assigned to `conn` in `with`

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("[INFO] Database connection closed.")
        if exc_type:
            print(f"[ERROR] {exc_type}: {exc_val}")
        # returning False will re-raise exceptions if they happen
        return False

# ✅ Use the context manager
with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
