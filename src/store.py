"""Fake — in-memory DB แทนของจริง."""
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    tier: str


class FakeDB:
    def __init__(self):
        self.users: dict[int, User] = {}

    def save(self, user: User) -> None:
        self.users[user.id] = user

    def get(self, user_id: int) -> User | None:
        return self.users.get(user_id)
