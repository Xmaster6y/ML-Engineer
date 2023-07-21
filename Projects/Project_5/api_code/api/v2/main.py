"""
v2 API module.
"""

import logging
import os

from fastapi import FastAPI

app = FastAPI(
    title="Tag API v2",
    description="Second version of the Tag API.",
)


@app.on_event("startup")
async def startup_event():
    """
    Startup hook event.
    """
    logger = logging.getLogger("uvicorn")
    logger.info("Starting up API v2...")


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
