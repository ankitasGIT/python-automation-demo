# Petstore API Test Suite – Solution Documentation

This document explains the test cases written for the Petstore API. Each section describes what a test is meant to verify, how it behaves, and what outcome is expected. The goal is to make the intent of every test clear and easy to understand.

---

## Table of Contents
1. [Setting Up Virtual Environment](#setting-up-virtual-environment)
2. [Troubleshooting](#troubleshooting)
3. [Running the Tests](#running-the-tests)
4. [Pet Endpoint Tests](#pet-endpoint-tests)
5. [Store / Order Endpoint Tests](#store--order-endpoint-tests)
6. [Test Fixtures](#test-fixtures)
7. [Schema Validation](#schema-validation)
8. [Bugs and Fixes](#bugs-and-fixes)

---



## Setting Up Virtual Environment

### Prerequisites

Before setting up the virtual environment, ensure you have the following installed:
- Python 3.7 or higher


### Step 1: Create Virtual Environment

Navigate to the project root directory and create a virtual environment:

```bash
# Navigate to project directory
cd /pytest-api-example-main

# Create virtual environment named 'venv'
python3 -m venv venv # On macOS

python -m venv venv  # On windows 
```

### Step 2: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt once activated.


## Troubleshooting

### Issue: ModuleNotFoundError - No module named 'app'

**Error Message:**
```
ImportError while loading conftest 'tests/conftest.py'.
tests/conftest.py:20: in <module>
    import app as app_module
ModuleNotFoundError: No module named 'app'
```



Run this command before executing pytest:
```bash
export PYTHONPATH=.
```


---


## Running the Tests

**Run all tests:**
```bash
pytest
```

**Run specific test file:**
```bash
pytest tests/test_store.py -v
pytest tests/test_pet.py -v
```


---

## Pet Endpoint Tests

### 1. `test_pet_schema()`

**File:** `tests/test_pet.py`

This test checks whether the API returns a pet object in the correct format.

The test sends a request to fetch a pet with ID `1` using the `/pets/1` endpoint. It then verifies that the request succeeds and that the response data follows the schema defined for a pet in `schemas.py`.

The test expects a successful response (`200 OK`) and a JSON object containing fields like `id`, `name`, `type`, and `status`.

**Assertions:**
- Response status code is `200`
- Response body matches the pet schema

---

### 2. `test_find_by_status_200(status)`

**File:** `tests/test_pet.py`

This test validates the `/pets/findByStatus` endpoint, which returns pets filtered by their status.

It is parameterized to run for each valid status: `available`, `sold`, and `pending`. For each status value, the test sends a request with that status as a query parameter.

**Assertions:**
- Response status code is `200`
- Every pet in the response has the requested status
- Each pet object follows the pet schema

---

### 3. `test_get_by_id_404(pet_id)`

**File:** `tests/test_pet.py`

This test focuses on invalid or edge-case pet IDs.

It is parameterized with inputs such as negative numbers, non-existent IDs, floats, strings, special characters, and invalid text values. For each input, the test attempts to fetch a pet using `/pets/{pet_id}`.

**Assertions:**
- Response status code is `404` for all invalid inputs

---

## Store / Order Endpoint Tests


---

### 4. `test_place_order_pet_not_available_returns_400()` – Case 2

**File:** `tests/test_store.py`

This test checks that the API rejects orders for pets that are not available.

An order is attempted for `pet_id` `1`, which has status `pending`.

**Assertions:**
- Response status code is `400 Bad Request`


---

### 5. `test_patch_order_by_id(client)`

**File:** `tests/test_store.py`

This test ensures that updating an order also updates the associated pet's status.

Steps:
1. Create an order for `pet_id` `2`
2. Update the order status to `sold`
3. Fetch the pet again to confirm status update

**Assertions:**
- Order creation returns `201`
- PATCH request returns `200`
- Response message confirms update
- Pet status is updated to `sold`

---

### 6. `test_patch_order_to_available_updates_pet_status(client)`

**File:** `tests/test_store.py`

This test checks that updating an order's status to `available` also updates the pet's status.

Steps:
1. Create an order for `pet_id` `0`
2. Update the order status to `available`

**Assertions:**
- PATCH request returns `200`
- Pet status is updated to `available`

---

### 7. `test_patch_order_not_found_returns_404(client)`

**File:** `tests/test_store.py`

This test verifies the behavior when attempting to update a non-existent order.

A fake order ID is used in a PATCH request.

**Assertions:**
- Response status code is `404 Not Found`

---

### 8. `test_patch_order_invalid_status_returns_400(client)`

**File:** `tests/test_store.py`

This test ensures that invalid order status values are rejected.

Steps:
1. Create a valid order
2. Attempt to update the order with an invalid status value

**Assertions:**
- Order creation returns `201`
- PATCH request returns `400 Bad Request`

---

### 9. `test_order_schema_with_valid_data(client)`

**File:** `tests/test_store.py`

This test validates the structure of the order response.

An order is created and the response JSON is validated against the order schema defined in `schemas.py`.

**Assertions:**
- Response status code is `201`
- Response body matches the order schema

---

## Test Fixtures

### `client` Fixture

**File:** `tests/conftest.py`

The `client` fixture provides a clean test environment for every test.

Before each test:
- All pets are reset to their initial state
- All orders are cleared
- A Flask test client is created

This ensures test isolation and consistent results.

---

## Schema Validation

### Pet Schema

The pet schema defines the required fields, data types, and allowed values for a pet object, including valid `type` and `status` values.

---

### Order Schema

The order schema defines the required structure of an order object, ensuring that mandatory fields are present and that the status value is valid.


---





## Bugs and Fixes

### Bug 1: Invalid Pet Name Type in schemas.py

**Issue:**
In `schemas.py`, the `name` field in the pet schema was incorrectly defined as `Integer` type instead of `String`.

**Location:** `schemas.py` - Pet schema properties

**Original Code:**
```python
pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "integer"  # Wrong - should be string
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        ...
    }
}
```

---

### Bug 2: Unformatted Print Statement in app.py

**Issue:**
At line 101 in `app.py`, a formatted string was created but not used in the print statement.

**Location:** `app.py` - Line 101

**Original Code:**
```python
if status not in PET_STATUS:
    api.abort(400, 'Invalid pet status {status}')   # Wrong - not using format string
```




---
















