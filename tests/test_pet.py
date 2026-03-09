from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_


def test_pet_schema():
    """
        Validates:
            - Single pet object matches the expected schema
    """
    test_endpoint = "/pets/1"

    response = api_helpers.get_api_data(test_endpoint)

    assert response.status_code == 200

    # Validate the response schema against the defined schema in schemas.py
    validate(instance=response.json(), schema=schemas.pet)


@pytest.mark.parametrize("status", [("available"), ("sold"), ("pending")])
def test_find_by_status_200(status):
    """
    Test that the /pets/findByStatus endpoint returns pets filtered by status.
    
    Validates:
    - Response status code is 200
    - Each pet in the response has the matching status value
    - Each pet object matches the expected schema
    
    Args:
        status: Pet status to filter by ('available', 'sold', or 'pending')
    """
    test_endpoint = "/pets/findByStatus"
    params = {
        "status": status
    }

    response = api_helpers.get_api_data(test_endpoint, params)
    data = response.json()

    assert response.status_code == 200

    for pet in data:
        assert pet['status'] == status
        validate(instance=pet, schema=schemas.pet)

@pytest.mark.parametrize("pet_id", [-1, 9999, 5, 1.22, "6", "one","&^%*","null","undefined"])
def test_get_by_id_404(pet_id):
    """
    Test that the /pets/{pet_id} endpoint returns 404 for invalid or non-existent pet IDs.
    
    Validates:
    - Response status code is 404 for various edge cases including negative IDs,
      non-existent IDs, floats, empty strings, and non-numeric values
    
    Args:
        pet_id: Invalid or non-existent pet ID to test
    """
    test_endpoint = f"/pets/{pet_id}"
    
    response = api_helpers.get_api_data(test_endpoint)

    assert_that(response.status_code, is_(404))

