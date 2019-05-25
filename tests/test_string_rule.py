from yuko.rules import String
from yuko.schema import Schema


def test_string_required():
    class TestSchema(Schema):
        name = String(required=True)

    test_schema = TestSchema()
    test_schema.validate({'bad-key': 'value'})

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'name': ['can not be blank']}


def test_string_allow_null():
    class TestSchema(Schema):
        name = String(allow_null=True)

    test_schema = TestSchema()
    test_schema.validate({'name': None})

    assert test_schema.has_errors is False
    assert test_schema.as_dict() == {}


def test_string_bad_type():
    class TestSchema(Schema):
        name = String()

    test_schema = TestSchema()
    test_schema.validate({'name': 10})

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'name': ['must be a string']}


def test_string_bad_length():
    class TestSchema(Schema):
        name = String(length=10)

    test_schema = TestSchema()
    test_schema.validate({'name': 'bad' * 20})

    error_msg = f'{test_schema.name.INCORRECT_LENGTH_ERROR} ' \
        f'{test_schema.name.length} characters'

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'name': [error_msg]}
