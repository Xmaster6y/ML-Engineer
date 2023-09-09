"""
API schemas.
"""

from typing import List, Optional

from pydantic import BaseModel, validator


class Tag(BaseModel):
    """
    Tag schema.
    """

    label: str
    probability: Optional[float]
    popularity: int

    @validator("probability")
    def probability_must_be_between_0_and_1(cls, value):
        """
        Validate probability.
        """
        if value is not None and (value < 0 or value > 1):
            raise ValueError("probability must be between 0.5 and 1")
        return value

    @validator("popularity")
    def popularity_must_be_positive(cls, value):
        """
        Validate popularity.
        """
        if value <= 0:
            raise ValueError("popularity must be positive")
        return value


class TagResponse(BaseModel):
    """
    Tag response schema.
    """

    tag_list: List[Tag]


class ErrorResponse(BaseModel):
    """
    Error response schema.
    """

    error: str
