"""Shared test fixtures for StadiumIQ test suite."""

import pytest

from app import create_app
from models import Stadium, db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def sample_stadium(app):
    """Create a sample stadium."""
    with app.app_context():
        stadium = Stadium(
            name="Test Stadium",
            city="Test City",
            country="USA",
            capacity=50000,
            latitude=34.0522,
            longitude=-118.2437,
        )
        db.session.add(stadium)
        db.session.commit()
        yield stadium
