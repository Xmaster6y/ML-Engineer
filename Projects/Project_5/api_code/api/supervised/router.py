"""
Supervised module router.
"""

import logging

from api.schema import TagResponse
from api.supervised import models
from api.supervised.constants import ALL_MODELS
from api.supervised.schema import SupervisedTagRequest
from fastapi import APIRouter

router = APIRouter()


@router.on_event("startup")
async def startup_event():
    """
    Startup hook event.
    """
    logger = logging.getLogger("uvicorn")
    logger.info("Supervised router starting up...")
    logger.info("Loading supervised models...")
    models.init_models()


@router.get("/info")
async def info():
    return {"all_models": ALL_MODELS}


@router.post(
    "/tag",
    response_model=TagResponse,
)
def tag(request: SupervisedTagRequest):
    """
    Tag.
    """
    title = request.title
    body = request.body
    n_tag_requested = request.n_tag_requested
    model_name = request.model_name

    tag_list = models.all_wrapped_models[model_name](title, body)

    return {"tag_list": tag_list[:n_tag_requested]}
