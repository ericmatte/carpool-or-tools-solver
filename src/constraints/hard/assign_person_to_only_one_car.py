from constraints.input import ConstraintInput
from utils.cp_helper import CPHelper


def assign_person_to_only_one_car(input: ConstraintInput, _helpers: CPHelper):
    """Each person can only be assigned to one car."""
    for person in input.people:
        assigned_to_cars = [input.person_to_car[(person.id, car.id)] for car in input.cars]
        input.model.Add(sum(assigned_to_cars) <= 1)
