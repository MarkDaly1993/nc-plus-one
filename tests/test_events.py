import pytest
from main import app
from fastapi.testclient import TestClient
from db.test_setup_files.connection_test import get_connection_to_database_test
from db.test_setup_files.test_seed import seed


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
    


