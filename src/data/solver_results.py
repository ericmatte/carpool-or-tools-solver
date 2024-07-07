import logging

from data.car import Car
from data.person import Person


class CarWithPeople:
    def __init__(self, car: Car, passengers: list[Person]):
        self.car = car
        self.passengers = passengers


class SolverResults:
    def __init__(self, cars_with_people_results: dict[str, list[str]], people: list[Person], cars: list[Car]):
        self._json = cars_with_people_results
        self.people = people
        self.cars = cars
        self.cars_with_people: list[CarWithPeople] = []
        self.unused_cars: list[Car] = []
        all_passengers: list[Person] = []

        for car in cars:
            passengers = [person for person in people if person.id in cars_with_people_results.get(car.id, [])]
            if len(passengers) > 0:
                self.cars_with_people.append(CarWithPeople(car, passengers))
                all_passengers.extend(passengers)
            else:
                self.unused_cars.append(car)

        self.unassigned_people = [person for person in people if person not in all_passengers]

    @property
    def json(self):
        return self._json

    def __repr__(self) -> str:
        return str(self._json)

    def print(self):
        if logging.getLogger().isEnabledFor(logging.INFO):
            logging.info("")
            people_assigned_count = sum(len(car.passengers) for car in self.cars_with_people)
            logging.info(f"Number of person assignations met = {people_assigned_count} / {len(self.people)}.")
            logging.info("")

            for car_with_people in self.cars_with_people:
                car = car_with_people.car
                passengers = car_with_people.passengers
                logging.info(f"{car.owner.name} ({car.make} {car.model}, {len(passengers)}/{car.seats} seats):")
                for person in passengers:
                    logging.info(f"  - {person.name}")
            logging.info("")

            if len(self.unused_cars) > 0:
                logging.info("Unused cars:")
                for car in self.unused_cars:
                    logging.info(f"  - {car.owner.name} ({car.make} {car.model}, {car.seats} seats)")
                logging.info("")

            if len(self.unassigned_people) > 0:
                logging.info("Unassigned people:")
                for person in self.unassigned_people:
                    logging.info(f"  - {person.name}")
                logging.info("")
