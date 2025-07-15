import aiosqlite
import asyncio

# ✅ Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        print("[ALL USERS]", users)
        return users

# ✅ Async function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        older_users = await cursor.fetchall()
        print("[USERS > 40]", older_users)
        return older_users

# ✅ Run both concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# ✅ Run the event loop
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
