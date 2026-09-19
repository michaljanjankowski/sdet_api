from pydantic import BaseModel, Field


class Resource1PostRequest(BaseModel):
    field1: str = Field(min_length=1)
    field2: str = Field(min_length=1)


class Resource1PutRequest(Resource1PostRequest):
    pass


class Resource1Response(Resource1PostRequest):
    id: int


class Resource1ListResponse(BaseModel):
    items: list[Resource1Response]
    total: int


class Resource1GetSpecialActionResponse(BaseModel):
    result: str
