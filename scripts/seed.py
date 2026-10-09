import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
from sqlalchemy.future import select
from app.database import AsyncSessionLocal, engine, Base
from app.models import User, Customer
from app.security import hash_password

async def seed_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        fake = Faker()

        # 1. Seed Admin User
        admin_email = "admin@example.com"
        result = await db.execute(select(User).filter(User.email == admin_email))
        existing_user = result.scalars().first()
        if not existing_user:
            hashed = hash_password("Welcome1@")
            admin = User(email=admin_email, hashed_password=hashed)
            db.add(admin)
            print(f"Created user: {admin_email}")

        # 2. Seed Customers
        result = await db.execute(select(Customer))
        existing_customers = result.scalars().all()
        if not existing_customers:
            for _ in range(25):
                c = Customer(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    phone=fake.phone_number(),
                    city=fake.city()
                )
                db.add(c)
            print("Created 25 fake customers.")

        await db.commit()
        print("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_db())
