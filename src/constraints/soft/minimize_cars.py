from ortools.sat.python.cp_model import IntVar

from constraints.input import ConstraintInput
from utils.cp_helper import CPHelper, Weight


def minimize_cars(input: ConstraintInput, helpers: CPHelper):
    """Minimize the number of different cars used for the carpool."""
    cars_used: list[IntVar] = []
    for car in input.cars:
        car_used = input.model.NewBoolVar(f"car_{car.id}_used")
        cars_used.append(car_used)
        for person in input.people:
            input.model.AddImplication(input.person_to_car[(person.id, car.id)], car_used)

    helpers.minimize(Weight.minimize_cars, sum(cars_used), len(input.cars))
