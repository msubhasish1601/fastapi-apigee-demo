from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, customers

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Apigee Demo API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(customers.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
