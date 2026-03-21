import sys
from pathlib import Path

# Add parent directory to path for local development
if __name__ == "__main__" or "backend" not in sys.modules:
    backend_dir = Path(__file__).resolve().parent
    parent_dir = backend_dir.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

from fastapi import FastAPI
from backend.routers import users
from contextlib import asynccontextmanager
from backend.crud.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (cleanup if needed)


app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def hello():
    return {"message": "Flight Booking API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="", port=8000)



# uvicorn main:app --reload