import logging
from typing import Any

from car_pool import CarPoolSolver, Constraint
from constraints.hard.assign_person_to_only_one_car import assign_person_to_only_one_car
from constraints.hard.owner_drives_when_passengers import owner_drives_when_passengers
from constraints.hard.seats_quantity import seats_quantity
from constraints.soft.maximize_seated_people import maximize_seated_people
from constraints.soft.minimize_cars import minimize_cars
from data.car import Car
from data.person import Person

CONSTRAINTS: list[Constraint] = [
    assign_person_to_only_one_car,
    owner_drives_when_passengers,
    seats_quantity,
    maximize_seated_people,
    minimize_cars,
]


logging.basicConfig(level=logging.INFO, format="%(levelname)s\t%(message)s")


def load_body(body: dict[str, Any]):
    people = [Person(person) for person in body["people"]]
    cars = [Car(car, people) for car in body["cars"]]
    return people, cars


def lambda_handler(body: dict[str, Any], _context: Any | None = None) -> dict[str, Any]:
    logging.info("Lambda started")
    try:
        people, cars = load_body(body)

        carPoolSolver = CarPoolSolver(people, cars, CONSTRAINTS)
    except Exception as error:
        return {"success": False, "message": f"{type(error).__name__}: {error}"}

    logging.info(f"Solving with {len(CONSTRAINTS)} constraints: {', '.join([c.__name__ for c in CONSTRAINTS])}")
    result = carPoolSolver.solve()
    logging.info(f"Done: Success: {result['success']}, Status: {result['status']}, SolutionsCount: {result.get('solutions_count', 0)}.")
    return result
