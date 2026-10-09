from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings
import ssl
from urllib.parse import urlparse, urlencode, parse_qsl, urlunparse

db_url = settings.database_url
connect_args = {}

parsed = urlparse(db_url)
query_params = dict(parse_qsl(parsed.query))

ssl_enabled = False
if query_params.get("sslmode") == "require" or query_params.get("ssl") == "require":
    ssl_enabled = True

# Safely remove parameters that break asyncpg
query_params.pop("sslmode", None)
query_params.pop("ssl", None)
query_params.pop("channel_binding", None)

parsed = parsed._replace(query=urlencode(query_params))
db_url = urlunparse(parsed)

if ssl_enabled:
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
