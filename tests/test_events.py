
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_events():
    response = client.get("/events")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_event():
    event_data = {
        "title": "Pytest Test Event",
        "description": "Testing event creation",
        "event_date": "2026-12-20",
        "location": "Islamabad",
        "max_capacity": 50
    }

    response = client.post("/events", json=event_data)

    assert response.status_code == 201
    assert response.json()["title"] == "Pytest Test Event"
    assert response.json()["max_capacity"] == 50

def test_create_event_invalid_capacity():
    event_data = {
        "title": "Invalid Event",
        "description": "Testing invalid capacity",
        "event_date": "2026-12-20",
        "location": "Islamabad",
        "max_capacity": 0
    }

    response = client.post("/events", json=event_data)

    assert response.status_code == 422

def test_update_event():
    event_data = {
        "title": "Event Before Update",
        "description": "Testing update",
        "event_date": "2026-12-20",
        "location": "Islamabad",
        "max_capacity": 50
    }

    create_response = client.post("/events", json=event_data)

    event_id = create_response.json()["id"]

    update_data = {
        "title": "Event After Update",
        "max_capacity": 100
    }

    response = client.put(
        f"/events/{event_id}",
        json=update_data
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Event After Update"
    assert response.json()["max_capacity"] == 100

def test_delete_event():
    event_data = {
        "title": "Event To Delete",
        "description": "Testing event deletion",
        "event_date": "2026-12-20",
        "location": "Islamabad",
        "max_capacity": 50
    }

    create_response = client.post("/events", json=event_data)

    event_id = create_response.json()["id"]

    response = client.delete(f"/events/{event_id}")

    assert response.status_code == 204

def test_create_registration():
    event_data = {
        "title": "Registration Test Event",
        "description": "Testing employee registration",
        "event_date": "2026-12-20",
        "location": "Islamabad",
        "max_capacity": 2
    }

    create_response = client.post("/events", json=event_data)
    event_id = create_response.json()["id"]

    registration_data = {
        "employee_name": "Ali",
        "employee_email": "ali.test@example.com"
    }

    response = client.post(
        f"/events/{event_id}/registrations",
        json=registration_data
    )

    assert response.status_code == 201
    assert response.json()["employee_email"] == "ali.test@example.com"

def test_duplicate_registration():
    event_data = {
        "title": "Duplicate Registration Test",
        "description": "Testing duplicate prevention",
        "event_date": "2026-12-20",
        "location": "Islamabad",
        "max_capacity": 5
    }

    create_response = client.post("/events", json=event_data)
    event_id = create_response.json()["id"]

    registration_data = {
        "employee_name": "Sara",
        "employee_email": "sara.test@example.com"
    }

    first_response = client.post(
        f"/events/{event_id}/registrations",
        json=registration_data
    )

    second_response = client.post(
        f"/events/{event_id}/registrations",
        json=registration_data
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409

def test_event_capacity_limit():
    event_data = {
        "title": "Capacity Test Event",
        "description": "Testing event capacity",
        "event_date": "2026-12-20",
        "location": "Islamabad",
        "max_capacity": 1
    }

    create_response = client.post("/events", json=event_data)
    event_id = create_response.json()["id"]

    first_registration = {
        "employee_name": "Ali",
        "employee_email": "ali.capacity@example.com"
    }

    second_registration = {
        "employee_name": "Sara",
        "employee_email": "sara.capacity@example.com"
    }

    first_response = client.post(
        f"/events/{event_id}/registrations",
        json=first_registration
    )

    second_response = client.post(
        f"/events/{event_id}/registrations",
        json=second_registration
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409

def test_registration_for_nonexistent_event():
    registration_data = {
        "employee_name": "Ahmed",
        "employee_email": "ahmed.test@example.com"
    }

    response = client.post(
        "/events/999999/registrations",
        json=registration_data
    )

    assert response.status_code == 404

def test_read_event_registrations():
    event_data = {
        "title": "View Registrations Test",
        "description": "Testing registration retrieval",
        "event_date": "2026-12-20",
        "location": "Islamabad",
        "max_capacity": 5
    }

    create_response = client.post("/events", json=event_data)
    event_id = create_response.json()["id"]

    registration_data = {
        "employee_name": "Ahmed",
        "employee_email": "ahmed.view@example.com"
    }

    client.post(
        f"/events/{event_id}/registrations",
        json=registration_data
    )

    response = client.get(
        f"/events/{event_id}/registrations"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["employee_name"] == "Ahmed"

def test_delete_registration():
    event_data = {
        "title": "Delete Registration Test",
        "description": "Testing registration deletion",
        "event_date": "2026-12-20",
        "location": "Islamabad",
        "max_capacity": 5
    }

    create_response = client.post("/events", json=event_data)
    event_id = create_response.json()["id"]

    registration_data = {
        "employee_name": "Sara",
        "employee_email": "sara.delete@example.com"
    }

    registration_response = client.post(
        f"/events/{event_id}/registrations",
        json=registration_data
    )

    registration_id = registration_response.json()["id"]

    response = client.delete(
        f"/registrations/{registration_id}"
    )

    assert response.status_code == 204
