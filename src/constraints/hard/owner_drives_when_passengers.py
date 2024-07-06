from constraints.input import ConstraintInput
from data.person import Person
from utils.cp_helper import CPHelper


def owner_drives_when_passengers(input: ConstraintInput, helpers: CPHelper):
    """The owner of the car must drive when there are passengers in the car."""
    for car in input.cars:
        owner = car.owner
        possible_passengers = [person for person in input.people if person.id != owner.id]

        def is_in_car(person: Person):
            return input.person_to_car[(person.id, car.id)]

        owner_must_drive = helpers.vars.new_bool(f"car_{car.id}_owner_drives")

        input.model.Add(is_in_car(owner) == 1).OnlyEnforceIf(owner_must_drive)
        for person in possible_passengers:
            input.model.AddImplication(is_in_car(person), owner_must_drive)
