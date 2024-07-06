import json
import logging
from typing import Any, Literal, cast

from handler import lambda_handler
from scripts.run import read_file

TEST_FILE = "tests/mocks/payload.json"


def get_mock_payload(mock: Literal["overflow", "one_car", "two_cars", "three_cars"]):
    return json.loads(read_file(f"tests/mocks/{mock}.json"))


def solve(body: Any):
    result = lambda_handler(body, None)
    logging.debug(f"Result: {result}")
    assert result["success"] == True
    assert result["status"] == "optimal"
    return result


class TestSolve:
    def test_must_solve_mock(self):
        body = get_mock_payload("overflow")

        solve(body)

    def test_return_400_if_empty_body(self):
        body = lambda_handler(cast(Any, None))
        assert body["success"] == False
        assert "NoneType" in body["message"]

    def test_return_400_if_invalid_body(self):
        body = lambda_handler({"invalid": "body"})
        assert body["success"] == False
        assert "KeyError" in body["message"]
