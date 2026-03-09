import copy
import pytest
import app as app_module


@pytest.fixture()
def client(monkeypatch):
    """
    Flask test client + reset in-memory storage for each test.
    """
    base_pets = copy.deepcopy(app_module.pets)
    base_orders = {}

    # Patch module-level globals used by routes
    monkeypatch.setattr(app_module, "pets", copy.deepcopy(base_pets), raising=False)
    monkeypatch.setattr(app_module, "orders", copy.deepcopy(base_orders), raising=False)

    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client