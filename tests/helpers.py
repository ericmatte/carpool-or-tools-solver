import json
import logging
from typing import Any, Literal

from handler import lambda_handler
from scripts.run import read_file


def get_mock_payload(mock: Literal["overflow", "one_car", "two_cars", "three_cars"]):
    return json.loads(read_file(f"tests/mocks/{mock}.json"))


def solve(body: Any):
    result = lambda_handler(body, None)
    logging.debug(f"Result: {result}")
    assert result["success"] == True
    assert result["status"] == "optimal"
    return result
