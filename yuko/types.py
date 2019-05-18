"""Validation type classes"""
import typing

from .validator import AbstractValidator


class Number:
    __slots__ = ('minimum', 'maximum', 'between')

    def __init__(
        self,
        minimum: int = None,
        maximum: int = None,
        between: tuple = None
    ):
        self.minimum = minimum
        self.maximum = maximum
        self.between = between


class Integer(Number, AbstractValidator):
    _INSTANCE = int

    def __init__(
        self,
        minimum: int = None,
        maximum: int = None,
        between: tuple = None,
    ):
        super().__init__(minimum, maximum, between)

    def validate(self, key: str, value: typing.Any):
        pass

    def key_present(self):
        pass
