"""
Main API module.
"""

from api.v1 import app as v1_app
from fastapi import FastAPI

app = FastAPI()

app.mount("/v1", v1_app)
