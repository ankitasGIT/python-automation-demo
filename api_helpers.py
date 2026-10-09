"""
API Helpers Module

This module provides helper functions to communicate with the Flask Petstore API
using HTTP requests.

The module supports three types of HTTP operations:
- GET: Retrieve data from API endpoints.
- POST: Send data to create new resources.
- PATCH: Update existing resources partially.

The base URL points to the locally running Flask application at
http://127.0.0.1:5000.

Usage:
    get_api_data('/pets/')
    post_api_data('/pets/', {'id': 3, 'name': 'Buddy', 'type': 'dog'})
    patch_api_data('/store/order/<order_id>', {'status': 'sold'})

Note:
    Ensure the Flask API server is running before calling these functions.
"""
import requests

base_url = 'http://127.0.0.1:5000'

# GET requests
def get_api_data(endpoint, params = {}):
    response = requests.get(f'{base_url}{endpoint}', params=params)
    return response

# POST requests
def post_api_data(endpoint, data):
    response = requests.post(f'{base_url}{endpoint}', json=data)
    return response

# PATCH requests
def patch_api_data(endpoint, data):
    response = requests.patch(f'{base_url}{endpoint}', json=data)
    return response
