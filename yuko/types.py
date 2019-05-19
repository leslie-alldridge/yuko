"""Validation type classes"""
import typing

from .schema import Schema
from .validator import AbstractValidator


class Number(Schema):
    # TODO: Add description for this class

    # Error messages
    INVALID_MAXIMUM_LENGTH_ERROR = 'must be not greater than'
    INVALID_MINIMUM_LENGTH_ERROR = 'must be greater than'
    KEY_NOT_PRESENT_ERROR = 'can not be blank'

    __slots__ = ('minimum', 'maximum', 'between', '_errors', 'required')

    def __init__(
            self,
            minimum: int = None,
            maximum: int = None,
            between: tuple = None,
            required: bool = None):

        self.minimum = minimum
        self.maximum = maximum
        self.between = between
        self.required = required
        self._errors = []

    def key_not_present(self, key: str) -> typing.NoReturn:
        self.errors[key] = [self.KEY_NOT_PRESENT_ERROR]

    def maximum_is_valid(self, value: int) -> bool:
        return value <= self.maximum

    def minimum_is_valid(self, value: int) -> bool:
        return value >= self.minimum

    def between_is_valid(self, value: int) -> bool:
        return self.between[0] <= value <= self.between[1]

    def push_error(self, error: str) -> typing.NoReturn:
        self._errors.append(error)


class Integer(Number, AbstractValidator):
    # TODO: Add description for this class

    # Base type of a correct value
    _INSTANCE = int

    # Error messages
    INVALID_TYPE = 'must be an integer'

    def __init__(
            self,
            minimum: int = None,
            maximum: int = None,
            between: tuple = None,
            required: bool = None):
        super().__init__(minimum, maximum, between, required)

    def process(self, key: str, value: typing.Any) -> typing.NoReturn:
        if not isinstance(value, self._INSTANCE):
            self._errors.append(self.INVALID_TYPE)
            self.errors[key] = self._errors
            return

        if self.maximum and not self.maximum_is_valid(value):
            self.push_error(f'{self.INVALID_MAXIMUM_LENGTH_ERROR} {self.maximum}')

        if self.minimum and not self.minimum_is_valid(value):
            self.push_error(f'{self.INVALID_MINIMUM_LENGTH_ERROR} {self.minimum}')

        if self.between and not self.between_is_valid(value):
            self.push_error(
                f'value must be between {self.between[0]}'
                f' and {self.between[1]}'
            )

        if not self._errors:
            return

        self.errors[key] = self._errors

    def key_not_present(self, key: str) -> typing.NoReturn:
        super().key_not_present(key)
