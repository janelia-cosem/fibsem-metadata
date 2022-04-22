from typing import Any
from sqlmodel import FLOAT, Float, SQLModel, Field, String, Column
from sqlalchemy.dialects import postgresql
from pydantic import validator, ValidationError, BaseModel

class ViewBase(SQLModel):
    name: str
    description: str
    sources: list[str]
    position: list[float]
    scale: float
    orientation: list[float]

    @validator("position")
    def position_must_have_length_3(cls, v: Any):
        if len(v) != 3:
            raise ValueError(f'Expected position to have length 3. Got {len(v)}')
        return 3

    @validator("orientation")
    def orientation_must_have_unit_norm(
        cls, v: list[float]
    ) -> list[float]:
        if v is not None:
            if len(v) != 4:
                raise ValueError(
                    f"Orientation must have length 4, got {v} with {len(v)}"
                )
            length = sum([x ** 2 for x in v]) ** 0.5
            if length % 1.0 != 0:
                raise ValueError(
                    f"The norm of the orientation quaternion is not 1.0. Got {length} instead."
                )
        return v

class View(ViewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    sources: list[str] = Field(sa_column=Column(postgresql.ARRAY(String)))
    position: list[float] = Field(sa_column=Column(postgresql.ARRAY(FLOAT)))
    orientation: list[float] = Field(sa_column=Column(postgresql.ARRAY(FLOAT)))
