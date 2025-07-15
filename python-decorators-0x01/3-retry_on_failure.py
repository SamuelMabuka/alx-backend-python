import time
import sqlite3 
import functools

# ✅ Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
            print("[INFO] Database connection closed.")
    return wrapper

# ✅ Decorator to retry function on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    print(f"[INFO] Attempt {attempt + 1}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"[WARN] Error: {e}")
                    if attempt < retries:
                        print(f"[INFO] Retrying after {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("[ERROR] Max retries reached. Raising error.")
                        raise
        return wrapper
    return decorator

# ✅ Function to fetch users with connection and retry decorators
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# ✅ Run it
users = fetch_users_with_retry()
print(users)
