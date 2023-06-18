from fastapi import HTTPException
from events.models import Event

async def create_event(event_name: str, event_uri: str):
    return {"message": "Event created successfully"}