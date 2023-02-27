from typing import Optional, List
import uuid
from pydantic import BaseModel, Field


class Model(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    uid: str = Field(...)
    sha_auth_code: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "uid": "U71104f51176a5b84c2fe5555cb88275f",
                "sha_auth_code": "9113e4f37ce44ef6ac0b466309c8e45a6014d4de3b9c54c4e7f8c12ec51e1732",
            }
        }


class updateModel(BaseModel):
    uid: Optional[str]
    sha_auth_code: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "uid": "update uid",
                "sha_auth_code": "update sha 256",
            }
        }
