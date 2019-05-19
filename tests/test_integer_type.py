"""Test integer type"""
import orjson

from yuko.schema import Schema
from yuko.types import Integer


def test_integer_correct_validation():
    class TestSchema(Schema):
        age = Integer(minimum=1, maximum=5)

    test_schema = TestSchema()
    test_schema.validate({'age': 4})

    assert test_schema.is_valid is True
    assert test_schema.as_dict() == {}


def test_integer_required():
    class TestSchema(Schema):
        age = Integer(required=True)

    test_schema = TestSchema()
    test_schema.validate({'invalid': None})

    assert test_schema.is_valid is False
    assert test_schema.as_dict() == {'age': ['can not be blank']}


def test_integer_minimum():
    class TestSchema(Schema):
        age = Integer(minimum=2)

    test_schema = TestSchema()
    test_schema.validate({'age': 1})

    assert test_schema.is_valid is False
    assert test_schema.as_dict() == {'age': [f'must be greater than {test_schema.age.minimum}']}


def test_integer_bad_type():
    class TestSchema(Schema):
        age = Integer()

    test_schema = TestSchema()
    test_schema.validate({'age': 'bad type'})

    assert test_schema.is_valid is False
    assert test_schema.as_dict() == {'age': ['must be an integer']}


def test_integer_between():
    class TestSchema(Schema):
        age = Integer(between=(1, 10))

    test_schema = TestSchema()
    test_schema.validate({'age': 15})

    error = f'value must be ' \
        f'between {test_schema.age.between[0]}' \
        f' and {test_schema.age.between[1]}'

    assert test_schema.is_valid is False
    assert test_schema.as_dict() == {'age': [error]}


def test_integer_json_output():
    class TestSchema(Schema):
        age = Integer(minimum=1)

    test_schema = TestSchema()
    test_schema.validate({'age': 0})

    expected_json = orjson.dumps({'age': ['must be greater than 1']})

    assert test_schema.is_valid is False
    assert test_schema.as_json() == expected_json
