"""
Semi-supervised models.
"""

import json
import logging
from typing import Dict, List

import openai
from api.constants import TAG_LIST
from api.schema import Tag
from api.semisupervised.constants import (
    ALL_MODELS,
    OPENAI_API_KEY,
    PROMPT_TEMPLATE,
)


def find_popular_tags(s):
    if isinstance(s, list):
        return [(rs, TAG_LIST.index(rs)) for rs in s if rs in TAG_LIST]
    s = str(s)
    s.replace("'", '"')
    global TAG_LIST
    raw_splits = s.split('"')
    return [(rs, TAG_LIST.index(rs)) for rs in raw_splits if rs in TAG_LIST]


def extract_tags(response):
    logger = logging.getLogger("uvicorn")
    try:
        d = json.loads(response)
        try:
            tags = d["label"]
            return find_popular_tags(tags)
        except Exception as e:
            logger.info(e)
        try:
            tags = d["labels"]
            return find_popular_tags(tags)
        except Exception as e:
            logger.info(e)
            logger.info(d)
    except Exception as e:
        logger.info(e)
    return find_popular_tags(response)


class WrappedSemisupervisedModel:
    """
    Wrapper for supervised model.
    """

    def __init__(self, model_name: str):
        self.config: dict = ALL_MODELS[model_name]

    def __call__(self, title, body_text, body_code) -> List[Tag]:
        logger = logging.getLogger("uvicorn")
        if self.config["model_type"] != "openai":
            raise NotImplementedError(
                f"Model type {self.config['model_type']} not supported."
            )
        openai.api_key = OPENAI_API_KEY
        prompt = PROMPT_TEMPLATE.format(
            labels=TAG_LIST,
            title=title,
            body_text=body_text,
            body_code=body_code,
        )
        completion = openai.ChatCompletion.create(
            model=self.config["model_name"],
            messages=[
                {
                    "role": "system",
                    "content": "You are a text classification model.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        info = completion["choices"][0]["message"]["content"]
        usage = completion["usage"]
        logger.info(f"Usage: {usage}")
        logger.info(f"Info: {info}")
        tag_index_l = extract_tags(info)
        return [
            Tag(
                label=tag,
                probability=None,
                popularity=index + 1,
            )
            for tag, index in tag_index_l
        ]


all_wrapped_models: Dict[str, WrappedSemisupervisedModel] = {}


def init_models():
    """
    Load models.
    """
    logger = logging.getLogger("uvicorn")
    global all_wrapped_models
    logger.info("Wrapping supervised models...")
    for alias_name in ALL_MODELS:
        all_wrapped_models[alias_name] = WrappedSemisupervisedModel(alias_name)
        logger.info(f"Semi-supervised model {alias_name} wrapped.")
    logger.info("Semi-supervised models wrapped.")
