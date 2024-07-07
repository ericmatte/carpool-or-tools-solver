import json
import logging
from typing import Any, Literal

from data.solver_results import SolverResults
from handler import lambda_handler
from scripts.run import read_file


# Must match .vscode/launch.json inputs
def get_mock_payload(mock: Literal["overflow", "one_car", "two_cars", "three_cars", "impossible"]):
    return json.loads(read_file(f"tests/mocks/{mock}.json"))


def solve(body: Any):
    result = lambda_handler(body, None)
    logging.debug(f"Result: {result}")
    assert result["status"] == "optimal"
    assert result["success"] == True
    solver_results: SolverResults = result["result"]
    return solver_results
