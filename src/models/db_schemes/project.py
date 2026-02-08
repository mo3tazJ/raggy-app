from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    # Custom validator example
    @field_validator('project_id')
    def validate_project_id(cls, value: str):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value

    model_config = ConfigDict(arbitrary_types_allowed=True)
    # class config:
    #     arbitrary_types_allowed = True