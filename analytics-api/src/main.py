from fastapi import FastAPI
from api.events import router as evntRouter
from contextlib import asynccontextmanager
from api.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Starting up...")
    init_db()
    yield
    # Shutdown code
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(evntRouter, prefix="/api/events", tags=["events"])

@app.get("/")
def read_root():
    return {"Hello": "World fastapi"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}



# uvicorn main:app --reload
