from typing import Generic, TypeVar

from pydantic import BaseModel

ResponseT = TypeVar("ResponseT", bound=BaseModel)


class ErrorResponse(BaseModel):
    error: str


class EmptyResponse(BaseModel):
    pass


class ResponseInfo(BaseModel, Generic[ResponseT]):
    response: ResponseT | ErrorResponse
    response_status: int

    def check_status(self, expected_status: int) -> None:
        assert self.response_status == expected_status, (
            f"Expected HTTP {expected_status}, got {self.response_status}: {self.response}"
        )
