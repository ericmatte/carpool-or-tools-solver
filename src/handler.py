import logging
from typing import Any

from car_pool_solver import CarPoolSolver
from data.car import Car
from data.person import Person

logging.basicConfig(level=logging.INFO, format="%(levelname)s\t%(message)s")


def load_body(body: dict[str, Any]):
    people = [Person(person) for person in body["people"]]
    cars = [Car(car, people) for car in body["cars"]]
    return people, cars


def lambda_handler(body: dict[str, Any], _context: Any | None = None) -> dict[str, Any]:
    logging.info("Lambda started")
    try:
        people, cars = load_body(body)
        car_pool_solver = CarPoolSolver(people, cars)
    except Exception as error:
        return {"success": False, "message": f"{type(error).__name__}: {error}"}

    result = car_pool_solver.solve()
    logging.info(f"Done: Success: {result['success']}, Status: {result['status']}, SolutionsCount: {result.get('solutions_count', 0)}.")
    return result
