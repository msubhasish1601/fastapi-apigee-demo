import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test():
    # Use a dummy URL with ssl=require to trigger the SQLAlchemy ssl logic
    engine = create_async_engine("postgresql+asyncpg://postgres:fake@localhost/fake?ssl=require")
    try:
        async with engine.connect() as conn:
            pass
    except Exception as e:
        print(f"Error type: {type(e)}")
        print(f"Error: {e}")

asyncio.run(test())
