from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, customers

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Apigee Demo API", lifespan=lifespan)

# Enable CORS so our HTML frontend can talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(customers.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
