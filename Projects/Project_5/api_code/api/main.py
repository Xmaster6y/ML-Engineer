"""
Main API module.
"""


from api.v1 import app as app_v1
from api.v2 import app as app_v2
from fastapi import FastAPI

app = FastAPI(
    title="Tag API",
    description="""
# API for Tagging Stack Overflow Questions

This API allows you to tag Stack Overflow questions with the appropriate tags.

## API Version 1

- [Swagger UI](/v1/docs)
- [Redoc](/v1/redoc)

Only implements a single endpoint for tagging questions.

## API Version 2

- [Swagger UI](/v2/docs)
- [Redoc](/v2/redoc)
""",
)


@app.get(
    "/",
    tags=["HOME"],
    summary="Home page",
)
async def home():
    return {"message": "Welcome to the Tag API!"}


app.mount("/v1", app_v1)
app.mount("/v2", app_v2)
