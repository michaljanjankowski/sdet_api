"""Typed client for the fixed responses served by MockServer."""

import httpx
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str


class User(UserCreate):
    id: int


class UsersClient:
    def __init__(self, base_url: str, timeout: float = 1.0) -> None:
        self.client = httpx.Client(base_url=base_url, timeout=timeout)

    def close(self) -> None:
        self.client.close()

    def list_users(self) -> list[User]:
        response = self.client.get("/users")
        response.raise_for_status()
        return [User.model_validate(item) for item in response.json()]

    def get_user(self, user_id: int) -> User:
        response = self.client.get(f"/users/{user_id}")
        response.raise_for_status()
        return User.model_validate(response.json())

    def create_user(self, user: UserCreate) -> User:
        response = self.client.post("/users", json=user.model_dump())
        response.raise_for_status()
        return User.model_validate(response.json())

    def delete_user(self, user_id: int) -> None:
        response = self.client.delete(f"/users/{user_id}")
        response.raise_for_status()

    def get_slow(self) -> dict:
        response = self.client.get("/slow")
        response.raise_for_status()
        return response.json()

    def get_error(self) -> None:
        response = self.client.get("/error")
        response.raise_for_status()
