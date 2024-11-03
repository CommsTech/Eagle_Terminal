import pytest

from ai.chief import Chief


@pytest.fixture
def chief():
    return Chief()


def test_chief_initialization():
    chief = Chief(user_id="test_user")
    assert chief is not None
