from fastapi import APIRouter
from events.views import create_event

events_router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

events_router.add_api_route("/create", create_event, methods=["POST"])
