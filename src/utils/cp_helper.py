from enum import Enum
from typing import Sequence

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntegralT, IntVar, LinearExpr, _ProductCst, _Sum

from constraints.input import ConstraintInput

infinity = cp_model.INT32_MAX


class Weight(Enum):
    """Weight for the objectives, to balance them. Higher weight means higher priority."""

    maximize_seated_people = 5
    minimize_cars = 1


class CPHelper:
    def __init__(self, input: ConstraintInput):
        self.input = input
        self._vars_to_maximise: list[IntegralT | LinearExpr] = []

    def maximize(self, weight: Weight, value: LinearExpr | int, max_value: int):
        self._set_objective(weight.name, value, max_value, weight.value)

    def minimize(self, weight: Weight, value: LinearExpr | int, max_value: int):
        self._set_objective(weight.name, value, max_value, -weight.value)

    def apply_objectives(self):
        """Maximise all the objectives at once, since we can only have one main objective allowed in the CP model."""
        self.input.model.Maximize(sum(self._vars_to_maximise))

    def max(self, name: str, values: Sequence[IntVar | _Sum | _ProductCst | int]):
        """max() from python is interpreted before the Add() method is called.
        The result is unpredictable, and therefore we need to use the AddMaxEquality method from the CP model.
        This returns the maximum value variable of the list of values.
        """
        max_overtime_day = self.input.model.NewIntVar(0, infinity, name)
        self.input.model.AddMaxEquality(max_overtime_day, values)
        return max_overtime_day

    def _set_objective(self, name: str, value: LinearExpr | int, max_value: int, weight: int):
        target = self.input.model.NewIntVar(-infinity, infinity, name)
        num = self.input.model.NewIntVar(-infinity, infinity, f"{name}_num")
        self.input.model.Add(num == value * 100)

        self.input.model.AddDivisionEquality(target, num, max_value)
        self._vars_to_maximise.append(target * weight)
