"""Test integer type"""
import orjson

from yuko.rules import Integer
from yuko.schema import Schema


def test_integer_allow_null():
    class TestSchema(Schema):
        age = Integer(allow_null=True, maximum=5)

    test_schema = TestSchema()
    test_schema.validate({'age': None})

    assert test_schema.has_errors is False
    assert test_schema.as_dict() == {}

    test_schema.validate({'age': 3})

    assert test_schema.has_errors is False
    assert test_schema.as_dict() == {}

    test_schema.validate({'age': 10})

    expected_error = {'age': [f'must be less than {test_schema.age.maximum}']}

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == expected_error


def test_integer_minimum():
    class TestSchema(Schema):
        age = Integer(minimum=1)

    test_schema = TestSchema()
    test_schema.validate({'age': 0})

    expected_error = {'age': [f'must be greater than {test_schema.age.minimum}']}
    assert test_schema.has_errors is True
    assert test_schema.as_dict() == expected_error


def test_integer_maximum():
    class TestSchema(Schema):
        age = Integer(maximum=100)

    test_schema = TestSchema()
    test_schema.validate({'age': 101})

    expected_error = {'age': [f'must be less than {test_schema.age.maximum}']}

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == expected_error


def test_integer_required():
    class TestSchema(Schema):
        age = Integer(required=True)

    test_schema = TestSchema()
    test_schema.validate({'another': 'key'})

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'age': ['can not be blank']}


def test_integer_between():
    class TestSchema(Schema):
        age = Integer(between=(1, 43))

    test_schema = TestSchema()
    test_schema.validate({'age': 44})

    error = f'must be between {test_schema.age.between[0]} ' \
        f'and {test_schema.age.between[1]}'

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'age': [error]}


def test_integer_bad_type():
    class TestSchema(Schema):
        age = Integer()

    test_schema = TestSchema()
    test_schema.validate({'age': 'str'})

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'age': ['must be an integer']}


def test_integer_json():
    class TestSchema(Schema):
        age = Integer(maximum=5)

    test_schema = TestSchema()
    test_schema.validate({'age': 10})

    expected_error = orjson.dumps(
        {'age': [f'must be less than {test_schema.age.maximum}']}
    )

    assert test_schema.has_errors is True
    assert test_schema.as_json() == expected_error


def test_integer_two_values():
    class TestSchema(Schema):
        age = Integer()
        price = Integer(maximum=100)

    test_schema = TestSchema()
    test_schema.validate({'age': 10, 'price': 200})

    expected_error = {'price': [f'must be less than {test_schema.price.maximum}']}

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == expected_error


def test_integer_invalid_validation_two_values():
    class TestSchema(Schema):
        age = Integer(required=True)
        price = Integer(maximum=100)

    test_schema = TestSchema()
    test_schema.validate({'bad-key': None, 'price': 200})

    expected_errors = {
        'age': ['can not be blank'],
        'price': [f'must be less than {test_schema.price.maximum}'],
    }

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == expected_errors


def test_integer_required_two_values():
    class TestSchema(Schema):
        age = Integer(required=True)
        price = Integer(required=True)

    test_schema = TestSchema()
    test_schema.validate({'bad-key': None, 'second-bad-key': 200})

    expected_errors = {
        'age': ['can not be blank'],
        'price': ['can not be blank'],
    }

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == expected_errors
