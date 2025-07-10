import time
import sqlite3 
import functools

query_cache = {}

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"[CACHE] Using cached result for query: {query}")
            return query_cache[query]
        print(f"[CACHE MISS] Query not cached. Executing: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# Connection handler
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call — query runs and result is cached
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call — cached result is returned
users_again = fetch_users_with_cache(query="SELECT * FROM users")