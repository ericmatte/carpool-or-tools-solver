from enum import Enum
from typing import Sequence

from ortools.sat.python.cp_model import IntegralT, IntVar, LinearExpr, _ProductCst, _Sum

from constraints.input import ConstraintInput
from utils.vars_manager import VarsManager, infinity


class Weight(Enum):
    """Weight for the objectives. Higher weight means higher priority."""

    maximize_seated_people = 5
    minimize_cars = 1


class CPHelper:
    def __init__(self, input: ConstraintInput, vars: VarsManager):
        self.input = input
        self.vars = vars
        self._expressions_to_maximise: list[IntegralT | LinearExpr] = []

    def maximize(self, weight: Weight, value: LinearExpr | int, max_value: int):
        self._set_objective(weight.name, value, max_value, weight.value)

    def minimize(self, weight: Weight, value: LinearExpr | int, max_value: int):
        self._set_objective(weight.name, value, max_value, -weight.value)

    def max(self, name: str, values: Sequence[IntVar | _Sum | _ProductCst | int]):
        """max() from python is interpreted before the Add() method is called.
        The result is unpredictable, so we must use the AddMaxEquality method from the CP model.
        """
        max_overtime_day = self.vars.new_int(name, min=0, max=infinity)
        self.input.model.AddMaxEquality(max_overtime_day, values)
        return max_overtime_day

    def apply_objectives(self):
        """Maximise all objectives at once, since we can only have one main objective used by the CP model."""
        self.input.model.Maximize(sum(self._expressions_to_maximise))

    def _set_objective(self, name: str, value: LinearExpr | int, max_value: int, weight: int):
        target = self.vars.new_int(name)
        num = self.vars.new_int(f"{name}_value")
        self.input.model.Add(num == value * 100)

        self.input.model.AddDivisionEquality(target, num, max_value)
        self._expressions_to_maximise.append(target * weight)
