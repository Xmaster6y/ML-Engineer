"""
Supervised models.
"""

import logging
import pickle
from typing import Any, Dict, List

import numpy as np
from api.constants import TAG_LIST
from api.schema import Tag
from api.supervised.constants import ALL_MODELS
from sentence_transformers import SentenceTransformer

all_embeddings: Dict[str, SentenceTransformer] = {}
all_models: Dict[str, Any] = {}


class WrappedSupervisedModel:
    """
    Wrapper for supervised model.
    """

    def __init__(self, model_name: str):
        self.config: dict = ALL_MODELS[model_name]

    def __call__(self, title, body_text, body_code) -> List[Tag]:
        if self.config["embedding_model"] is not None:
            if not self.config["embed_targets"]:
                raise ValueError("embed_targets must not be empty")
            # Embed title and body
            embeddings = []
            global all_embeddings
            titlecode = title + "\n\n" + body_code  # noqa: F841
            titletext = title + "\n\n" + body_text  # noqa: F841
            for target in self.config["embed_targets"]:
                embeddings.append(
                    all_embeddings[self.config["embedding_model"]].encode(
                        [eval(target)]
                    )
                )
            # Concatenate embeddings
            embedding = np.concatenate(embeddings, axis=1)
        else:
            raise NotImplementedError("No embedding model is specified")
        # Predict
        global all_models
        logger = logging.getLogger("uvicorn")
        logger.info(f"Embedding shape: {embedding.shape}")
        all_proba = np.array(
            all_models[self.config["model_name"]].predict_proba(embedding)
        )
        logger.info(f"Proba shape: {all_proba.shape}")
        try:
            proba = all_proba[:, 0, 1]
        except:  # noqa: E722
            proba = all_proba[0, :]
        # Get top tags
        top_tags = np.argsort(proba)[::-1]
        tag_list = [
            Tag(
                label=TAG_LIST[tag_index],
                probability=proba[tag_index],
                popularity=tag_index + 1,
            )
            for tag_index in top_tags
        ]
        return tag_list


all_wrapped_models: Dict[str, WrappedSupervisedModel] = {}


def init_models():
    """
    Load models.
    """
    logger = logging.getLogger("uvicorn")
    logger.info("Loading embedding models...")
    global all_embeddings
    all_names = set(
        [config["embedding_model"] for config in ALL_MODELS.values()]
    )
    for name in all_names:
        all_embeddings[name] = SentenceTransformer(name)
        logger.info(f"Embedding model {name} loaded.")
    logger.info("Embedding models loaded.")

    global all_models
    logger.info("Loading supervised models...")
    all_names = set([config["model_name"] for config in ALL_MODELS.values()])
    for name in all_names:
        with open(f"api/models/{name}.pkl", "rb") as f:
            all_models[name] = pickle.load(f)
        logger.info(f"Supervised model {name} loaded.")
    logger.info("Models loaded.")

    global all_wrapped_models
    logger.info("Wrapping supervised models...")
    for alias_name in ALL_MODELS:
        all_wrapped_models[alias_name] = WrappedSupervisedModel(alias_name)
        logger.info(f"Supervised model {alias_name} wrapped.")
    logger.info("Supervised models wrapped.")
