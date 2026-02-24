import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module

# Keep an original deep copy of the in-memory state so tests can reset it
ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the module-level `activities` dict before each test."""
    app_module.activities = copy.deepcopy(ORIGINAL_ACTIVITIES)
    yield
    app_module.activities = copy.deepcopy(ORIGINAL_ACTIVITIES)


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    with TestClient(app_module.app) as c:
        yield c
