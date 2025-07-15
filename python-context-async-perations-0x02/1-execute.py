import sqlite3

# ✅ Class-based context manager to run a query with parameters
class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        print("[INFO] Running query...")
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("[INFO] Database connection closed.")
        if exc_type:
            print(f"[ERROR] {exc_type}: {exc_val}")
        return False  # propagate exceptions if any

# ✅ Example usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("users.db", query, params) as results:
    print("[RESULT]", results)
