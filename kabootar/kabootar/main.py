from fastapi import FastAPI
from fastapi.responses import FileResponse
from events.routes import events_router
from kabootar.config import settings

def create_application() -> FastAPI:

    application = FastAPI()

    application.include_router(events_router)

    return application

app = create_application()
