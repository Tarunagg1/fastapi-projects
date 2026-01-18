from  fastapi import APIRouter
import os
from .models import (
    EventModel,
    EventListSchema,
    EventUpdateSchema,
    EventCreateSchema
)


router = APIRouter()

@router.get("/")
def get_events() -> EventListSchema:
    print(os.getenv("DATABASE_URL"))
    return {"results": [
        {
            "id": 1
        }
    ],
     "count": 1}


@router.get("/{event_id}")
def get_event(event_id: int) -> EventModel:
    return {"id": event_id}

@router.put("/{event_id}")
def update_event(event_id: int, event: EventUpdateSchema) -> EventModel:
    return event


@router.post("/")
def create_event(payload: EventCreateSchema) -> EventModel:
    data = payload.model_dump()

    return {
        "id": 1,
        **data
    }

