"""
Main API module.
"""

import logging
import os

from api.v1.supervised import router as supervised_router
from fastapi import FastAPI

app = FastAPI(
    title="API v1",
    description="The first version of my API",
)


@app.on_event("startup")
async def startup_event():
    """
    Startup hook event.
    """
    logger = logging.getLogger("uvicorn")
    logger.info("Starting up...")


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
    return {k: v for k, v in os.environ.items()}


app.include_router(
    supervised_router,
    prefix="/supervised",
    tags=["SUPERVISED"],
)
