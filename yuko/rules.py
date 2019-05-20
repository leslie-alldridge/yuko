"""Validation type classes"""
import typing

from .rule import RuleInterface


class Number(RuleInterface):
    # TODO: Add description for this class

    # Error messages
    INVALID_MAXIMUM_LENGTH_ERROR = 'must be less than'
    INVALID_MINIMUM_LENGTH_ERROR = 'must be greater than'
    KEY_NOT_PRESENT_ERROR = 'can not be blank'

    __slots__ = (
        'minimum',
        'maximum',
        'between',
        '_errors',
        'required',
        'allow_null'
    )

    def __init__(
            self,
            minimum: int = None,
            maximum: int = None,
            between: tuple = None,
            required: bool = None,
            allow_null=False):

        self.minimum = minimum
        self.maximum = maximum
        self.between = between
        self.required = required
        self.allow_null = allow_null
        self._errors = []

    def maximum_is_valid(self, value: int) -> bool:
        return value <= self.maximum

    def minimum_is_valid(self, value: int) -> bool:
        return value >= self.minimum

    def between_is_valid(self, value: int) -> bool:
        return self.between[0] <= value <= self.between[1]

    def key_not_present(self) -> typing.List[str]:
        return [self.KEY_NOT_PRESENT_ERROR]


class Integer(Number):
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
            required: bool = None,
            allow_null=False):
        super().__init__(minimum, maximum, between, required, allow_null)

    def process(self, key: str, value: int) -> typing.List[str]:
        if self.allow_null and value is None:
            return

        if not isinstance(value, self._INSTANCE):
            self._errors.append(self.INVALID_TYPE)
            return self._errors

        if self.maximum and not self.maximum_is_valid(value):
            self._errors.append(
                f'{self.INVALID_MAXIMUM_LENGTH_ERROR} {self.maximum}'
            )

        if self.minimum and not self.minimum_is_valid(value):
            self._errors.append(
                f'{self.INVALID_MINIMUM_LENGTH_ERROR} {self.minimum}'
            )

        if self.between and not self.between_is_valid(value):
            self._errors.append(
                f'must be between {self.between[0]}'
                f' and {self.between[1]}'
            )

        if not self._errors:
            return

        return self._errors

    def key_not_present(self) -> typing.List[str]:
        return super().key_not_present()
