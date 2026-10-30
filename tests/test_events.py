import pytest
from main import app
from fastapi.testclient import TestClient
from db.test_setup_files.connection_test import get_connection_to_database_test
from db.test_setup_files.test_seed import seed
from jwt_token import create_access_token


#seeds the data each time a test is invoke. removes changes due to post and delete test.
@pytest.fixture(autouse=True)
def seed_test_db():
    connection = get_connection_to_database_test()
    seed(connection)

#uses TestClient to get a conection to the server
@pytest.fixture()
def client():
    return TestClient(app)

def test_get_events_responds_with200(client):
    response = client.get("/api/events")
    assert response.status_code == 200

def test_get_events_returns_a_list(client):
    response = client.get("/api/events")
    body = response.json()
    assert type(body['events']) == list

def test_get_events_returns_all_events(client):
    response = client.get("/api/events")
    body = response.json()
    assert len(body['events']) == 5

def test_get_event_returns_a_status_code_200(client):
    response = client.get("/api/events/1")
    assert response.status_code == 200

def test_get_event_returns_404_if_event_not_present(client):
    response = client.get("/api/events/6")
    assert response.status_code == 404


def test_get_event_returns_a_single_event(client):
    responce = client.get("/api/events/1")
    body = responce.json()
    assert len(body['event']) == 9

def test_get_event_returns_the_correct_event_based_on_id(client):
    response = client.get("/api/events/1")
    body = response.json()
    assert body['event']['title'] == 'event_d'

def test_get_event_only_returns_one_event(client):
    response = client.get("/api/events/1")
    body = response.json()
    assert len(body) == 1


def test_get_event_returns_400_if_id_is_invalid_type(client):
    response = client.get("/api/events/abc")
    assert response.status_code == 400

def test_create_rsvp_returns_201_if_given_the_correct_token(client):
    encoded_token = create_access_token(1)
    response = client.post("/api/events/1/rsvp", json={"token": encoded_token},)
    assert response.status_code== 201

def test_create_rsvp_returns_404_if_event_is_not_found(client):
    encoded_token = create_access_token(1)
    response = client.post("/api/events/6/rsvp", json={"token": encoded_token},)
    assert response.status_code== 404

def test_create_rsvp_returns_409_if_user_has_already_rsvped_for_that_event(client):
    encoded_token = create_access_token(1)
    response = client.post("/api/events/3/rsvp", json={"token": encoded_token},)
    assert response.status_code== 409

def test_create_rsvp_returns_204_if_rsvp_is_alrady_booked(client):
    response = client.delete("/api/events/3/rsvp/me", headers={"Authorization": f"Bearer {create_access_token(1)}"})
    assert response.status_code== 204

def test_create_rsvp_returns_401_if_the_token_is_missing(client):
    response = client.delete("/api/events/3/rsvp/me", headers={"Authorization": f"Bearer {''}"})
    assert response.status_code== 401

def test_create_rsvp_returns_401_if_the_token_does_not_have_bearer(client):
    response = client.delete("/api/events/3/rsvp/me", headers={"Authorization": create_access_token(1)})
    assert response.status_code== 401


def test_create_rsvp_returns_404_if_the_rsvp_does_not_exist_already(client):
    response = client.delete("/api/events/2/rsvp/me", headers={"Authorization": f"Bearer {create_access_token(1)}"})
    assert response.status_code== 404


