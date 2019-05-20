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

    def __init__(self):
        self.__errors = {}
        self.__has_errors = False

    def validate(self, data: dict) -> typing.NoReturn:
        """TODO: Add a comment"""
        for key in self.__collect_rules():

            rule = self.__class__.__dict__[key]
            if key not in data and rule.required:
                self.__errors[key] = rule.key_not_present()

            if key in data:
                rule_errors = self.__class__.__dict__[key].process(key, data[key])
                if rule_errors:
                    self.__errors[key] = rule_errors

        if self.__errors:
            self.__has_errors = True

    @property
    def has_errors(self):
        return self.__has_errors

    def as_json(self) -> typing.ByteString:
        """Returns a serialized Python object with errors"""
        return orjson.dumps(self.__errors)

    def as_dict(self) -> typing.Dict:
        """Returns dictionary with errors"""
        return self.__errors

    def __collect_rules(self) -> typing.List[str]:
        """TODO: Add a comment"""
        rules = [rule for rule in self.__class__.__dict__ if not rule.startswith('__')]
        return rules
