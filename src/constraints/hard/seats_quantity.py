from constraints.input import ConstraintInput
from utils.cp_helper import CPHelper


def seats_quantity(input: ConstraintInput, _helpers: CPHelper):
    """Validate that each car has the correct number of people assigned to it."""
    for car in input.cars:
        people_count = 0
        for person in input.people:
            people_count += input.person_to_car[(person.id, car.id)]

        input.model.Add(people_count <= car.seats)
