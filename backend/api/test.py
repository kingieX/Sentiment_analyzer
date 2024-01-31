import requests
from fastapi import status
import json
import asyncio




BASE_URL = 'http://127.0.0.1:8000/'


def test_info():
    info_url = BASE_URL + 'info'
    response = requests.get(info_url)
    assert response.status_code == 200
    assert response.json()
    print(response)


def test_signup():
    signup_url = BASE_URL + 'signup'
    user = {
        "username": "innocentchild",
        "fullname": "Ibiam Innocent",
        "email": f"innocentchild44@gmail.com",
        "password": "Test@password34",
    }

    response = requests.post(signup_url, json=user)
    assert response.json()
    print(response)

def test_login():
    login_url = BASE_URL + "login"

    test_user_data = {
        "email": "innocentchild44@gmail.com",
        "password": "Test@password34",
    }

    response = requests.post(login_url, json=test_user_data)

    # Assert status code
    assert response.status_code == status.HTTP_200_OK, f"Unexpected status code: {response.status_code}"

    # Assert access token presence
    assert "access_token" in response.json(), "Missing access token in response"

    # Assert refresh token presence
    assert "refresh_token" in response.json(), "Missing refresh token in response"



VALID_USER_EMAIL = "innocentchild44@gmail.com"
VALID_USER_PASSWORD = "Test@password34"

def test_change_password():
    change_password_url = BASE_URL + 'change-password'
    old_password = VALID_USER_PASSWORD
    new_password = "Newtestpassword113"
    change_password_data = {
    "email": VALID_USER_EMAIL,
    "old_password": old_password,
    "new_password": new_password,
    }
    change_password_response = requests.post(change_password_url, json=change_password_data)
    print(change_password_response.json)


def test_get_users():

   # Define query parameters
    params = {
        "page": 1,
        "per_page": 10,
        "sort_by": "id",
        "sort_order": "asc",
        "filter_by": None,
    }

    # Make the request with the defined parameters
    response = requests.get("http://127.0.0.1:8000/users", params=params)

    # Check if the request was successful (status code 200)
    assert response.status_code == 200

    # Add more assertions based on your expected response format
    response_json = response.json()
    print(response_json)

def test_read_user():
  
    ruser_url  =  "http://127.0.0.1:8000/users/3" 
    
    # Make the request to the endpoint
    response = requests.get(ruser_url)

    # Check if the request was successful (status code 200)
    assert response.status_code == 200
    if response.status_code == 404:
        assert "User not found" in response.text

def test_logout_successful():
    # Assuming you have a valid token for testing purposes
    valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDM2OTMxMjIsInN1YiI6IjQifQ.OswUt4t6BahPWFTZ533g9-iHurMXhQIv2DmIy9iCCJM"

    response = requests.post(f"{BASE_URL}logout", headers={"Authorization": f"Bearer {valid_token}"})

    assert response.status_code == 200
    assert response.json() == {"message": "Logout successful"}

def test_logout_invalid_token():
    # Assuming you have an invalid token for testing purposes
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDM2OTMxMjIsInN1YiI6IjQifQ"

    response = requests.post(f"{BASE_URL}logout", headers={"Authorization": f"Bearer {invalid_token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}



def test_create_text_success():
        # Replace with valid course data for testing
        textinput_data = {
            "text_content": "Programming is cool, thou it needs hardwork",
            "text_title": "Nitigrity of programming",
            "language": "English",
            "user_id": 4,
        }

        response = requests.post(f"{BASE_URL}textinput", json=textinput_data)

        # Check if the request was successful (status code 200 or 201 depending on your API)
        assert response.status_code, 201  # Adjust the status code as per your API

        # Add more assertions based on your expected response format
        response_json = response.json()
        print(response_json)

def test_read_textinput():
  
    textinput_url  =  f"{BASE_URL}textinputs" 
    
    # Make the request to the endpoint
    response = requests.get(textinput_url)

    # Check if the request was successful (status code 200)
    assert response.status_code == 200
    print(response)


def test_get_textinput():

    id = 1  # Replace with the desired course ID for testing

    # Send GET request to the /course/{id} endpoint
    response = requests.get(f"{BASE_URL}textinpu/{id}")

    # Assert status code
    assert response.status_code == 200

    # Assert response data structure
    data = response.json()
    assert "id" in data
    assert "text_content" in data
    assert "text_title" in data
    # Add more assertions based on your schema

    print(data)


def test_delete_textinput():
    # Assuming you have a course with ID 1 to delete
    id = 1
    
    # Send DELETE request
    response = requests.delete(f"{BASE_URL}textinput/delete/{id}")
    # Assert status code
    assert response.status_code == 204

def test_update_textinput():
    test_textinput_id = 3
    test_updated_data = {
        "text_content": "leukamia is not a deadly disease that easily kills",
        "text_title": "leukamia disease",
        "language":"English",
        "user_id": 1
    }

    # Send a PUT request to update a course by ID
    response = requests.put(f"{BASE_URL}update/textinput/{test_textinput_id}", json=test_updated_data)

    # Check if the request was successful (status code 200)
    assert response.status_code == 200

    # Add more assertions based on your expected response format
    response_json = response.json()
    print(response_json)


