from typing import Union
from fastapi import FastAPI
from api.events import router as evntRouter


app = FastAPI()

app.include_router(evntRouter, prefix="/api/events", tags=["events"])

@app.get("/")
def read_root():
    return {"Hello": "World fastapi"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}



# uvicorn main:app --reload
