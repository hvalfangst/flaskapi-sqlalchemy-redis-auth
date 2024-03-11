import pytest
from pydantic import ValidationError

from users.models import CreateUserRequest


def create_user_request(email, password, access):
    return CreateUserRequest(
        first_name="Darth",
        last_name="Vader",
        phone_number="987654321",
        address="Death Star, Sith Headquarters",
        email=email,
        password=password,
        ssn="987654321",
        access=access
    )


def test_create_user_request_fails_due_to_invalid_access_input():
    with pytest.raises(ValidationError) as exc_info:
        create_user_request("darth.vader@sith.com", "darkside123", "INVALID")

    expected_error = {
        'type': 'enum',
        'loc': ('access',),
        'msg': "Input should be 'READ', 'WRITE', 'MODIFY' or 'DELETE'",
        'input': 'INVALID',
        'ctx': {'expected': "'READ', 'WRITE', 'MODIFY' or 'DELETE'"}
    }

    actual_error = exc_info.value.errors()

    assert [expected_error] == actual_error


def test_create_user_request_fails_due_to_invalid_email_input():
    with pytest.raises(ValidationError) as exc_info:
        create_user_request("HANSOLOCANNOTSOLOME", "darkside123", "DELETE")

    expected_error = {
        'input': 'HANSOLOCANNOTSOLOME',
        'loc': ('email',),
        'msg': 'value is not a valid email address: The email address is not valid. '
               'It must have exactly one @-sign.',
        'type': 'value_error',
        'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}
    }

    actual_error = exc_info.value.errors()
    assert [expected_error] == actual_error


def test_create_user_request_fails_due_to_invalid_password_input():
    with pytest.raises(ValidationError) as exc_info:
        create_user_request("darth.vader@sith.com", 666, "DELETE")

    expected_error = \
        {'input': 666,
         'loc': ('password',),
         'msg': 'Input should be a valid string',
         'type': 'string_type',
         'url': 'https://errors.pydantic.dev/2.5/v/string_type'}

    actual_error = exc_info.value.errors()
    assert [expected_error] == actual_error
