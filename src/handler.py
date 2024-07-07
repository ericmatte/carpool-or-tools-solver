import logging
from typing import Any

from car_pool_solver import CarPoolSolver, Constraint
from constraints.hard.assign_person_to_only_one_car import assign_person_to_only_one_car
from constraints.hard.owner_drives_when_passengers import owner_drives_when_passengers
from constraints.hard.seats_quantity import seats_quantity
from constraints.soft.maximize_seated_people import maximize_seated_people
from constraints.soft.minimize_cars import minimize_cars
from data.car import Car
from data.person import Person

logging.basicConfig(level=logging.INFO, format="%(levelname)s\t%(message)s")


CONSTRAINTS: list[Constraint] = [
    assign_person_to_only_one_car,
    owner_drives_when_passengers,
    seats_quantity,
    maximize_seated_people,
    minimize_cars,
]


def parse_body(body: dict[str, Any]):
    people = [Person(person) for person in body["people"]]
    cars = [Car(car, people) for car in body["cars"]]
    return people, cars


def lambda_handler(body: dict[str, Any], _context: Any | None = None) -> dict[str, Any]:
    logging.info("Lambda started")
    try:
        people, cars = parse_body(body)
        car_pool_solver = CarPoolSolver(people, cars)
    except Exception as error:
        return {"success": False, "message": f"{type(error).__name__}: {error}"}

    result = car_pool_solver.solve(CONSTRAINTS)
    logging.info(f"Done: Found {result.get('solutions_count', 0)} solutions with '{result['status']}' status.")
    return result
