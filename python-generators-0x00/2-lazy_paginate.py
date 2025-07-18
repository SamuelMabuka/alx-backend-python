seed = __import__('seed')

def paginate_users(page_size, offset):
    """Fetches a page of users from the database at the given offset"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """Generator that yields one page of users at a time"""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size