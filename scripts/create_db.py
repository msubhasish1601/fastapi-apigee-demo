import asyncio
import asyncpg

async def create_db():
    try:
        # Connect to the default 'postgres' database to create the new one
        conn = await asyncpg.connect(user='postgres', password='Welcome1@', host='localhost', database='postgres')
        await conn.execute('CREATE DATABASE "fastapi-apigee-demo"')
        print("Database created successfully.")
        await conn.close()
    except asyncpg.exceptions.DuplicateDatabaseError:
        print("Database already exists.")
    except Exception as e:
        print(f"Error checking/creating database: {e}")

if __name__ == "__main__":
    asyncio.run(create_db())
