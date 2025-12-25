import copy
import pytest
from fastapi.testclient import TestClient
import src.app as appmod


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before each test to avoid leakage."""
    original = copy.deepcopy(appmod.activities)
    yield
    appmod.activities.clear()
    appmod.activities.update(original)


@pytest.fixture()
def client():
    return TestClient(appmod.app)
