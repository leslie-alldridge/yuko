"""Schema stuff"""
import typing

import orjson


class Schema:
    """Base Schema class

    It is a pretty simple class, for all `Schemas`
    which will contain validation attributes.
    It will provide a way to run validation for a `Schema`.

        Attributes::
            errors(dict): Validation classes use this attribute in order to
                collect all validation errors and etc.
            is_valid(bool): A flag which allows to know
                whether a Schema is valid after validation.

        Methods::
            # TODO: Add description for all instance methods.
    """
    errors = {}
    is_valid = True

    def validate(self, data: dict) -> typing.NoReturn:
        """TODO: Add a comment"""
        for key, validator in self.__collect_not_present_keys().items():
            if key not in data and validator.required:
                validator.key_not_present(key)

        for key, value in self.__class__.__dict__.items():
            if key in data:
                self.__class__.__dict__[key].process(key, data[key])

        if self.errors:
            self.is_valid = False

    def as_json(self) -> typing.ByteString:
        """Returns a serialized Python object with errors"""
        return orjson.dumps(self.errors)

    def as_dict(self) -> typing.Dict:
        """Returns dictionary with errors"""
        return self.errors

    def __collect_not_present_keys(self) -> typing.Dict:
        """TODO: Add a comment"""
        values = [value for value
                  in self.__class__.__dict__ if not value.startswith('__')]

        validators = {value: self.__class__.__dict__[value] for value in values}
        return validators
