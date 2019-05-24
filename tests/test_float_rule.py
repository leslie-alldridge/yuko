from yuko.rules import Float
from yuko.schema import Schema


def test_float_required():
    class TestSchema(Schema):
        price = Float(required=True)

    test_schema = TestSchema()
    test_schema.validate({'bad-key': 'bad-value'})

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'price': ['can not be blank']}


def test_float_maximum():
    class TestSchema(Schema):
        price = Float(maximum=10.00)

    test_schema = TestSchema()
    test_schema.validate({'price': 10.11})

    error_msg = f'must be less than {test_schema.price.maximum}'

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'price': [error_msg]}


def test_float_minimum():
    class TestSchema(Schema):
        price = Float(minimum=10.00)

    test_schema = TestSchema()
    test_schema.validate({'price': 9.99})

    error_msg = f'must be greater than {test_schema.price.minimum}'

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'price': [error_msg]}


def test_float_between():
    class TestSchema(Schema):
        price = Float(between=(1.00, 11.00))

    test_schema = TestSchema()
    test_schema.validate({'price': 12.00})

    error_msg = f'must be between {test_schema.price.between[0]}' \
        f' and {test_schema.price.between[1]}'

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'price': [error_msg]}


def test_float_allow_null():
    class TestSchema(Schema):
        price = Float(allow_null=True)

    test_schema = TestSchema()
    test_schema.validate({'price': None})

    assert test_schema.has_errors is False
    assert test_schema.as_dict() == {}


def test_float_only_positive():
    class TestSchema(Schema):
        price = Float(only_positive=True)

    test_schema = TestSchema()
    test_schema.validate({'price': -1.11})

    assert test_schema.has_errors is True
    assert test_schema.as_dict() == {'price': ['must be positive']}


def test_float_valid():
    class TestSchema(Schema):
        price = Float(required=True, maximum=10, minimum=1)

    test_schema = TestSchema()
    test_schema.validate({'price': 8})

    assert test_schema.has_errors is False
    assert test_schema.as_dict() == {}
