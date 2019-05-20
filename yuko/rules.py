"""Validation type classes"""
import typing

from .rule import RuleInterface


class Number(RuleInterface):
    # TODO: Add description for this class

    # Error messages
    MAXIMUM_LENGTH_ERROR = 'must be less than'
    MINIMUM_LENGTH_ERROR = 'must be greater than'
    NOT_POSITIVE_ERROR = 'must be positive'
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
            allow_null: bool = False,
            only_positive: bool = False):

        self.minimum = minimum
        self.maximum = maximum
        self.between = between
        self.required = required
        self.allow_null = allow_null
        self.only_positive = only_positive
        self._errors = []

    def maximum_is_valid(self, value: int) -> bool:
        return value <= self.maximum

    def minimum_is_valid(self, value: int) -> bool:
        return value >= self.minimum

    def between_is_valid(self, value: int) -> bool:
        return self.between[0] <= value <= self.between[1]

    def positive_is_valid(self, value: int) -> bool:
        return value >= 0

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
            allow_null: bool = False,
            only_positive: bool = False):
        super().__init__(
            minimum=minimum,
            maximum=maximum,
            between=between,
            required=required,
            allow_null=allow_null,
            only_positive=only_positive)

    def process(self, key: str, value: int) -> typing.List[str]:
        if self.allow_null and value is None:
            return

        if not isinstance(value, self._INSTANCE):
            self._errors.append(self.INVALID_TYPE)
            return self._errors

        if self.only_positive and not self.positive_is_valid(value):
            self._errors.append(f'{self.NOT_POSITIVE_ERROR}')

        if self.maximum and not self.maximum_is_valid(value):
            self._errors.append(
                f'{self.MAXIMUM_LENGTH_ERROR} {self.maximum}'
            )

        if self.minimum and not self.minimum_is_valid(value):
            self._errors.append(
                f'{self.MINIMUM_LENGTH_ERROR} {self.minimum}'
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
