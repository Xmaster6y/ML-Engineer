"""
Supervised module schema.
"""

from api.supervised.constants import ALL_MODELS
from pydantic import BaseModel, root_validator, validator


class SupervisedTagRequest(BaseModel):
    """
    Supervised tag request schema.
    """

    title: str
    body: str
    n_tag_requested: int = 1
    model_name: str = "default"

    @validator("n_tag_requested")
    def n_tag_requested_must_be_positive(cls, value):
        """
        Validate n_tag_requested.
        """
        if value <= 0:
            raise ValueError("n_tag_requested must be positive")
        return value

    @validator("model_name")
    def model_name_must_be_in_available_model_list(cls, value):
        """
        Validate model_name.
        """
        if value not in ALL_MODELS.keys():
            raise ValueError(f"model_name must be in {ALL_MODELS.keys()}")
        return value

    @root_validator(skip_on_failure=True)
    def check_n_tag_requested(cls, values):
        """
        Check n_tag_requested.
        """
        n_tag_requested = values.get("n_tag_requested")
        model_name = values.get("model_name", 1)
        if n_tag_requested > ALL_MODELS[model_name]["n_tag"]:
            raise ValueError(
                f"n_tag_requested must be less than or equal to "
                f"{ALL_MODELS[model_name]['n_tag']}"
            )
        return values
