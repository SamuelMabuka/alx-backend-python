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

# ✅ Decorator to manage transaction: commit if successful, rollback on error
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("[INFO] Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Transaction rolled back: {e}")
            raise
    return wrapper

# ✅ Function to update user email wrapped in both decorators
@with_db_connection 
@transact
