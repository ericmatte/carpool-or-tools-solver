from typing import Any, cast

from handler import lambda_handler
from tests.helpers import get_mock_payload, solve
from utils.solutionner import Status


class TestSolve:
    def test_must_assign_only_one_car(self):
        body = get_mock_payload("one_car")

        result = solve(body)

        assert len(result.unassigned_people) == 0
        assert len(result.cars_with_people) == 1
        assert len(result.cars_with_people[0].passengers) == len(result.people)

    def test_must_assign_two_cars(self):
        body = get_mock_payload("two_cars")

        result = solve(body)

        assert len(result.unassigned_people) == 0
        assert len(result.cars_with_people) == 2
        assert len(result.unused_cars) == 2

    def test_must_assign_three_cars(self):
        body = get_mock_payload("three_cars")

        result = solve(body)

        assert len(result.unassigned_people) == 0
        assert len(result.cars_with_people) == 3
        assert len(result.unused_cars) == 1

    def test_must_assign_as_much_as_possible(self):
        body = get_mock_payload("overflow")

        result = solve(body)

        assert len(result.unassigned_people) > 0
        assert len(result.cars_with_people) == len(result.cars)
        assert len(result.unused_cars) == 0

        for car in result.cars_with_people:
            assert len(car.passengers) == car.car.seats

    def test_wont_assign_if_no_cars(self):
        body = get_mock_payload("impossible")

        result = lambda_handler(body, None)
        assert result["status"] == Status.model_invalid.name

    def test_return_400_if_empty_body(self):
        body = lambda_handler(cast(Any, None))
        assert body["success"] == False
        assert "NoneType" in body["message"]

    def test_return_400_if_invalid_body(self):
        body = lambda_handler({"invalid": "body"})
        assert body["success"] == False
        assert "KeyError" in body["message"]
