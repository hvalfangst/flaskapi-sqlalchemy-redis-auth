import logging

import logging

import pytest
from pydantic import ValidationError

from users.users_bp import users_bp
from common.app_factory import create
from common.db import db as _db
from users.tests.settings import TestConfig
from users.models import CreateUserRequest, UpdateUserRequest
from users.repository import UsersRepository


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create([users_bp], TestConfig)
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def repository(db):
    return UsersRepository(database=db)


def create_request(phone_number, address):
    return CreateUserRequest(
        first_name="Luke",
        last_name="Skywalker",
        phone_number=phone_number,
        address=address,
        email="luke.skywalker@rebellion.com",
        password="theforce",
        ssn="123456789",
        access="WRITE"
    )


def test_create_user(repository):
    request = create_request("123456789", "Tatooine, Lars Homestead")
    repository.create(request)
    user = repository.get_by_email("luke.skywalker@rebellion.com")

    assert user is not None
    assert user.email == "luke.skywalker@rebellion.com"


def test_update_user(repository):
    original_request = create_request("123456789", "Tatooine, Lars Homestead")
    repository.create(original_request)

    user = repository.get_by_email("luke.skywalker@rebellion.com")

    assert user is not None
    assert user.phone_number == f"{original_request.phone_number}"
    assert user.address == f"{original_request.address}"

    updated_request = UpdateUserRequest(
        phone_number="987654321",
        address="Yavin 4, Rebel Base"
    )

    repository.update("luke.skywalker@rebellion.com", updated_request)
    updated_user = repository.get_by_email("luke.skywalker@rebellion.com")

    assert updated_user is not None
    assert updated_user.phone_number == f"{updated_request.phone_number}"
    assert updated_user.address == f"{updated_request.address}"


def test_list_users(repository):
    users = repository.list()

    assert isinstance(users, list)


def test_get_user_by_email(repository):
    request = create_request("123456789", "Tatooine, Lars Homestead")
    repository.create(request)

    user = repository.get_by_email("luke.skywalker@rebellion.com")
    assert user is not None
    assert user.email == "luke.skywalker@rebellion.com"


def test_delete_user_by_email(repository):
    request = create_request("123456789", "Tatooine, Lars Homestead")
    repository.create(request)

    user = repository.get_by_email("luke.skywalker@rebellion.com")
    assert user is not None
    assert user.email == "luke.skywalker@rebellion.com"

    repository.delete_by_email("luke.skywalker@rebellion.com")

    deleted_user = repository.get_by_email("luke.skywalker@rebellion.com")
    assert deleted_user is None

