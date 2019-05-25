"""Validation stuff"""
import typing


class RuleInterface:

    def process(self, key: typing.AnyStr, value: typing.Any) -> typing.NoReturn:
        """A method for a validation class

            Args:
                key(str): A key in a json/dictionary which will
                be validated.
                value(Any): A value which will be validated.
        """
        raise NotImplementedError(
            'AbstractValidator.process() must be implemented'
        )

    def key_not_present(self) -> typing.NoReturn:
        """Sets an error if a key doesn't present in a data object."""
        raise NotImplementedError(
            'AbstractValidator.key_not_present() must be implemented'
        )
