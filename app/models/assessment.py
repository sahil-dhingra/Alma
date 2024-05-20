from pydantic import BaseModel, Json
from typing import Any


class Assessment(BaseModel):
    assessment: Json[Any]