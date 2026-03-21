from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlmodel import select

from .models import (
    EventModel,
    EventListSchema,
    EventUpdateSchema,
    EventCreateSchema,
    get_utc_now,
)

from api.db.session import get_session
from sqlmodel import Session

router = APIRouter()

@router.post("/")
def create_event(payload: EventCreateSchema,session:Session = Depends(get_session)) -> EventModel:
    data = payload.model_dump()
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.get("/")
def get_events(duration: str = Query(default="1 day"),pages: List = Query(default=None),
    session: Session = Depends(get_session)) -> EventListSchema:
    query = select(EventModel).limit(10)
    results = session.exec(query).all()
    count = len(results)
    return EventListSchema(results=results, count=count)


@router.get("/{event_id}")
def get_event(event_id: int, session: Session = Depends(get_session)) -> EventModel:
    event = session.get(EventModel, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}")
def update_event(event_id: int, event: EventUpdateSchema, session: Session = Depends(get_session)) -> EventModel:
    db_event = session.get(EventModel, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    event_data = event.model_dump(exclude_unset=True)
    for key, value in event_data.items():
        setattr(db_event, key, value)
    db_event.update_at = get_utc_now()
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event


@router.delete("/{event_id}")
def delete_event(event_id: int, session: Session = Depends(get_session)) -> dict:
    event = session.get(EventModel, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return {"detail": "Event deleted successfully"}
