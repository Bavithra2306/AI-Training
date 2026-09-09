from routers.conversation_routers import router as conversation_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(conversation_router)