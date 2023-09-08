"""
Semi-supervised module schema.
"""

from api.semisupervised.constants import ALL_MODELS, LENGTH_LIMIT
from pydantic import BaseModel, root_validator, validator


class SemisupervisedTagRequest(BaseModel):
    """
    Supervised tag request schema.
    """

    title: str
    body_text: str
    body_code: str
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
    def check_length(cls, values):
        """
        Check length limit.
        """
        title = values.get("title")
        body_text = values.get("body_text")
        body_code = values.get("body_code")
        if len(title) + len(body_text) + len(body_code) > LENGTH_LIMIT:
            raise ValueError(
                "Total length of title, body_text, and body_code "
                "must be less than or equal to "
                f"{LENGTH_LIMIT}"
            )
        return values
