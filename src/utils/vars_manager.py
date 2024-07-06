import logging

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel, IntVar

from utils.solutionner import Solutionner

infinity = cp_model.INT32_MAX


class VarsManager:
    def __init__(self, model: CpModel):
        self._all: list[IntVar] = []
        self.model = model

    def new_bool(self, name: str):
        var = self.model.NewBoolVar(name)
        self._all.append(var)
        return var

    def new_int(self, name: str, min: int = -infinity, max: int = infinity):
        var = self.model.NewIntVar(min, max, name)
        self._all.append(var)
        return var

    def print(self, solutionner: Solutionner):
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(f"{len(self._all)} variables:")
            all_vars = {var.Name(): solutionner.Value(var) for var in self._all}
            logging.debug(all_vars)
