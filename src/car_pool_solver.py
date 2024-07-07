import logging
import sys
from typing import Any, Callable

from ortools.sat.python.cp_model import CpModel

from constraints.input import ConstraintInput
from data.car import Car
from data.person import Person
from data.solver_results import SolverResults
from utils.cp_helper import CPHelper
from utils.solutionner import Solutionner, Status
from utils.vars_manager import VarsManager

Constraint = Callable[[ConstraintInput, CPHelper], None]


def is_in_test():
    return "pytest" in sys.modules


class CarPoolSolver:
    def __init__(self, people: list[Person], cars: list[Car]):
        model = CpModel()
        self.vars = VarsManager(model)
        self.input = ConstraintInput(model, self.vars, people, cars)
        self.solutionner = Solutionner()

    def solve(self, constraints: list[Constraint]) -> dict[str, Any]:
        logging.info(f"Solving with {len(constraints)} constraints: {', '.join([c.__name__ for c in constraints])}")

        helpers = CPHelper(self.input, self.vars)
        for constraint in constraints:
            constraint(self.input, helpers)
        helpers.apply_objectives()

        status = self.solutionner.solve(self.input.model)
        if status in [Status.optimal, Status.feasible]:
            cars_with_people = self._filled_cars_with_people()
            result = SolverResults(cars_with_people, self.input.people, self.input.cars)
            helpers.vars.print(self.solutionner)
            result.print()
            return {
                "success": True,
                "status": status.name,
                "solutions_count": self.solutionner.solution_count,
                "result": result if is_in_test() else result.json,
            }
        else:
            return {"success": False, "status": status.name}

    def _filled_cars_with_people(self):
        return {car.id: [person.id for person in self.input.people if self._is_assigned(person, car)] for car in self.input.cars}

    def _is_assigned(self, person: Person, car: Car) -> bool:
        """Only works once the model has been solved."""
        return self.solutionner.Value(self.input.person_to_car[(person.id, car.id)]) == 1
