from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_
import uuid

def test_patch_order_by_id(client):
    create_resp = client.post("/store/order", json={"pet_id": 2})
    assert create_resp.status_code == 201
    order_id = create_resp.get_json()["id"]

    patch_resp = client.patch(
        f"/store/order/{order_id}",
        json={"status": "sold"}
    )

    assert patch_resp.status_code == 200
    body = patch_resp.get_json()

    assert body["message"] == "Order and pet status updated successfully"

    pet_resp = client.get("/pets/2")
    assert pet_resp.status_code == 200
    assert pet_resp.get_json()["status"] == "sold"

def test_place_order_pet_not_available_returns_400(client):
    resp = client.post("/store/order", json={"pet_id": 1})
    assert resp.status_code == 400


def test_patch_order_to_available_updates_pet_status(client):
    create_resp = client.post("/store/order", json={"pet_id": 0})
    assert create_resp.status_code == 201
    order_id = create_resp.get_json()["id"]

    patch_resp = client.patch(
        f"/store/order/{order_id}",
        json={"status": "available"}
    )

    assert patch_resp.status_code == 200

    pet_resp = client.get("/pets/0")
    assert pet_resp.status_code == 200
    assert pet_resp.get_json()["status"] == "available"

def test_patch_order_not_found_returns_404(client):
    fake_id = str(uuid.uuid4())

    resp = client.patch(
        f"/store/order/{fake_id}",
        json={"status": "sold"}
    )

    assert resp.status_code == 404

def test_patch_order_invalid_status_returns_400(client):
    create_resp = client.post("/store/order", json={"pet_id": 2})
    assert create_resp.status_code == 201
    order_id = create_resp.get_json()["id"]

    resp = client.patch(
        f"/store/order/{order_id}",
        json={"status": "INVALID"}
    )

    assert resp.status_code == 400

def test_order_schema_with_valid_data(client):
    """Test that order response matches the defined schema"""
    create_resp = client.post("/store/order", json={"pet_id": 2})
    
    assert create_resp.status_code == 201

    # Get the JSON response data
    order_data = create_resp.get_json()
    
    # Validate the response schema against the defined schema in schemas.py
    validate(instance=order_data, schema=schemas.order)

