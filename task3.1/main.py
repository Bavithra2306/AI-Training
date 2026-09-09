from fastapi import FastAPI
from middleware.request_id import RequestIDMiddleware
from routers.llm_routers import router as llm_router
from config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="logs/app.log",
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
   )

app.add_middleware(RequestIDMiddleware)

app.include_router(llm_router)