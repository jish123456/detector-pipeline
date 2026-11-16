from datetime import datetime

from pydantic import BaseModel, Field


class Reading(BaseModel):
    timestamp: datetime
    channel: int = Field(ge=0, le=15)
    count_rate: float = Field(allow_inf_nan=False)
