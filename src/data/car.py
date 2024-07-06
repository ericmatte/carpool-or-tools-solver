from typing import Any

from data.person import Person


class Car:
    def __init__(self, raw_car: dict[str, Any], people: list[Person]):
        self.id: str = raw_car["id"]
        self.make: str = raw_car["make"]
        self.model: str = raw_car["model"]
        self.seats: int = raw_car["seats"]
        self.owner = self._get_owner(raw_car["owner_id"], people)

    def _get_owner(self, owner_id: str, people: list[Person]) -> Person:
        for person in people:
            if person.id == owner_id:
                return person
        raise ValueError(f"Owner with id {owner_id} not found")
