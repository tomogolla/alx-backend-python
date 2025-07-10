import aiosqlite
import asyncio

# Fetch all users asynchronously
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as conn:
        async with conn.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("[ALL USERS]", results)
            return results

# Fetch users older than 40 asynchronously
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as conn:
        async with conn.execute("SELECT * FROM users WHERE age > 40") as cursor:
            results = await cursor.fetchall()
            print("[USERS > 40]", results)
            return results

# Run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Entry point to run the async tasks
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())