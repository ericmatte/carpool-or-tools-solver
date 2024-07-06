from typing import Any


class Person:
    def __init__(self, raw_person: dict[str, Any]):
        self.id: str = raw_person["id"]
        self.name: str = raw_person["name"]
