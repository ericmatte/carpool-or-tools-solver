import logging
from enum import Enum

from ortools.sat.cp_model_pb2 import CpSolverStatus
from ortools.sat.python.cp_model import CpModel, CpSolver, CpSolverSolutionCallback

TIME_LIMIT = 60.0  # seconds


class Status(Enum):
    optimal = CpSolverStatus.OPTIMAL
    feasible = CpSolverStatus.FEASIBLE
    infeasible = CpSolverStatus.INFEASIBLE
    model_invalid = CpSolverStatus.MODEL_INVALID
    unknown = CpSolverStatus.UNKNOWN


class Solutionner(CpSolverSolutionCallback):
    def __init__(self):
        CpSolverSolutionCallback.__init__(self)
        self.input = input
        self._status = Status.unknown
        self._feasible_solution_count = 0

    def on_solution_callback(self):
        """Called when a new feasible solution is found.
        Optimal solution will end the search and not call this method.
        https://github.com/google/or-tools/issues/1458#issuecomment-516045853
        """
        self._feasible_solution_count += 1

    @property
    def solution_count(self):
        if self._status == Status.optimal:
            return 1 + self._feasible_solution_count
        return self._feasible_solution_count

    def solve(self, model: CpModel):
        cp_solver = CpSolver()
        cp_solver.parameters.max_time_in_seconds = TIME_LIMIT
        self._status = Status(cp_solver.Solve(model, self))

        title, *stats = cp_solver.ResponseStats().split("\n")
        logging.debug(f"Found {self._feasible_solution_count} feasible solutions.")
        logging.debug(f"{title}")
        [logging.debug(f"  {l}") for l in stats]

        return self._status
