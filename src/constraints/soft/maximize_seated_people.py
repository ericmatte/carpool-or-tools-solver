from constraints.input import ConstraintInput
from utils.cp_helper import CPHelper, Weight


def maximize_seated_people(input: ConstraintInput, helpers: CPHelper):
    """Maximize the number of seated people."""
    seated_people = [input.person_to_car[(person.id, car.id)] for person in input.people for car in input.cars]

    helpers.maximize(Weight.maximize_seated_people, sum(seated_people), len(input.people))
