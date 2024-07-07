from typing import Any

from data.person import Person


class Car:
    def __init__(self, raw_car: dict[str, Any], people: list[Person]):
        self.id: str = raw_car["id"]
        self.make: str = raw_car["make"]
        self.model: str = raw_car["model"]
        self.seats: int = raw_car["seats"]
        self.owner = next(person for person in people if person.id == raw_car["owner_id"])
