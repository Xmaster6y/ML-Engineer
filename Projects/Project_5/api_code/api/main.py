"""
Main API module.
"""

import logging
import os

from api.constants import APP_ENV
from api.supervised.router import router as supervised_router
from fastapi import FastAPI

app = FastAPI(
    title="Tag API",
    description=f"""
# API for Tagging Stack Overflow Questions

This API allows you to tag Stack Overflow questions with the appropriate tags.

**Environment**: {APP_ENV}

## Supervised

Multi label classification using supervised learning models.

## Documentation

- [Swagger UI](/docs)
- [Redoc](/redoc)
""",
)


@app.on_event("startup")
async def startup_event():
    """
    Startup hook event.
    """
    logger = logging.getLogger("uvicorn")
    logger.info("Starting up API v1...")


@app.get(
    "/",
    tags=["HOME"],
    summary="Home page",
)
async def home():
    return {"message": "Home"}


@app.get(
    "/env",
    tags=["HOME"],
    summary="Environment variables",
)
async def env():
    return dict(os.environ)


app.include_router(
    supervised_router,
    prefix="/supervised",
    tags=["SUPERVISED"],
)
