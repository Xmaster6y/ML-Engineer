"""
Main API module.
"""

import logging
import os

from api.supervised.router import router as supervised_router
from fastapi import FastAPI

app = FastAPI()


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
    return dict(os.environ)


app.include_router(
    supervised_router,
    prefix="/supervised",
    tags=["SUPERVISED"],
)
