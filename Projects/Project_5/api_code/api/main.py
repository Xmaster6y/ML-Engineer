"""
Main API module.
"""

import logging
import os

from api.constants import APP_ENV
from api.semisupervised.router import router as semisupervised_router
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
    logger.info("Starting up API...")


@app.get(
    "/",
    tags=["HOME"],
    summary="Home page",
)
async def home():
    return {"message": "Home"}


if APP_ENV == "dev":

    @app.get(
        "/env",
        tags=["HOME"],
        summary="Environment variables",
    )
    async def env():
        env_d = dict(os.environ)
        for k in env_d:
            if "SECRET" in k or "TOKEN" in k or "KEY" in k or "PASSWORD" in k:
                env_d[k] = "********"
        return env_d


app.include_router(
    supervised_router,
    prefix="/supervised",
    tags=["SUPERVISED"],
)

app.include_router(
    semisupervised_router,
    prefix="/semisupervised",
    tags=["SEMI-SUPERVISED"],
)
