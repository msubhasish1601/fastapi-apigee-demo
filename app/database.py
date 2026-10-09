from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings
import ssl

db_url = settings.database_url
connect_args = {}

if "sslmode=require" in db_url or "ssl=require" in db_url:
    db_url = db_url.replace("?sslmode=require", "").replace("?ssl=require", "")
    db_url = db_url.replace("&sslmode=require", "").replace("&ssl=require", "")
    
    # Create a native Python SSL context to bypass SQLAlchemy's buggy string parsing
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connect_args["ssl"] = ssl_context

engine = create_async_engine(db_url, echo=True, connect_args=connect_args)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
