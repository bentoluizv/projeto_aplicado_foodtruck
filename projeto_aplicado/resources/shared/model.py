from datetime import datetime

from sqlalchemy import func
from sqlmodel import Field, SQLModel

from projeto_aplicado.utils import get_ulid_as_str


class BaseModel(SQLModel):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    created_at: datetime = Field(default_factory=func.now, nullable=False)
    updated_at: datetime = Field(default_factory=func.now, nullable=False)
