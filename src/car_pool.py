import logging
from typing import Any, Callable

from ortools.sat.python.cp_model import CpModel

from constraints.input import ConstraintInput
from data.car import Car
from data.person import Person
from utils.cp_helper import CPHelper
from utils.solutionner import Solutionner, Status

Constraint = Callable[[ConstraintInput, CPHelper], None]


class CarPoolSolver:
    def __init__(self, people: list[Person], cars: list[Car], constraints: list[Constraint]):
        self.model = CpModel()
        self.constraints = constraints
        self.input = ConstraintInput(self.model, people, cars)
        self.solutionner = Solutionner()

    def solve(self) -> dict[str, Any]:
        helpers = CPHelper(self.input)
        for constraint in self.constraints:
            constraint(self.input, helpers)
        helpers.apply_objectives()

        status = self.solutionner.solve(self.input.model)
        if status in [Status.optimal, Status.feasible]:
            cars_with_people = self._filled_cars_with_people()
            self.print_debug(cars_with_people)
            self.print_info(cars_with_people)
            return {
                "success": True,
                "status": status.name,
                "solutions_count": self.solutionner.solution_count,
                "cars_with_people": cars_with_people,
            }
        else:
            return {"success": False, "status": status.name}

    def _filled_cars_with_people(self):
        """Only works once the model has been solved."""
        return {car.id: [person.id for person in self.input.people if self._is_assigned(person, car)] for car in self.input.cars}

    def _is_assigned(self, person: Person, car: Car) -> bool:
        return self.solutionner.Value(self.input.person_to_car[(person.id, car.id)]) == 1

    def print_debug(self, cars_with_people: dict[str, list[str]]):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            # TODO: Add cleaner logs
            # for name, var in self.input.person_to_car.items():
            #     logging.debug(f"  - {name} = {self.solutionner.Value(var)}")
            pass

    def print_info(self, cars_with_people: dict[str, list[str]]):
        if logging.getLogger().isEnabledFor(logging.INFO):

            people_count = len(self.input.people)
            people_assigned_count = sum([len(people) for people in cars_with_people.values()])
            unassigned_people = [
                person for person in self.input.people if all([not self._is_assigned(person, car) for car in self.input.cars])
            ]

            logging.info(f"Number of person assignations met = {people_assigned_count} / {people_count}.")
            logging.info("")

            unused_cars: list[Car] = []
            for car_id, people in cars_with_people.items():
                car = next((car for car in self.input.cars if car.id == car_id))
                if len(people) > 0:
                    logging.info(f"{car.owner.name} ({car.make} {car.model}, {len(people)}/{car.seats} seats):")
                    for person_id in people:
                        person = next((person for person in self.input.people if person.id == person_id))
                        logging.info(f"  - {person.name}")
                else:
                    unused_cars.append(car)
            logging.info("")

            if len(unused_cars) > 0:
                logging.info("Unused cars:")
                for car in unused_cars:
                    logging.info(f"  - {car.owner.name} ({car.make} {car.model}, {car.seats} seats)")
                logging.info("")

            if len(unassigned_people) > 0:
                logging.info("Unassigned people:")
                for person in unassigned_people:
                    logging.info(f"  - {person.name}")
                logging.info("")
