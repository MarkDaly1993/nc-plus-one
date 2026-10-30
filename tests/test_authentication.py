import pytest
from main import app
from fastapi.testclient import TestClient
from db.test_setup_files.connection_test import get_connection_to_database_test
from db.test_setup_files.test_seed import seed


@pytest.fixture(autouse=True)
def seed_test_db():
    connection = get_connection_to_database_test()
    seed(connection)
    print('seed')

@pytest.fixture()
def client():
    return TestClient(app)


def test_authernicate_user_responds_with200(client):
    response = client.post("/api/auth/login", json={"email": "user_c@example.com", "password": "password_c"},)
    assert response.status_code == 200

def test_authernicate_user_responds_with_400_if_email_is_missing(client):
    response = client.post("/api/auth/login", json={"password": "password_c"},)
    assert response.status_code == 400

def test_authernicate_user_responds_with_400_if_password_is_missing(client):
    response = client.post("/api/auth/login", json={"email": "user_c@example.com"},)
    assert response.status_code == 400

def test_authernicate_user_responds_with_401_if_password_is_incorrect(client):
    response = client.post("/api/auth/login", json={"email": "user_c@example.com", "password": "password_e"},)
    assert response.status_code == 401

def test_authernicate_user_responds_with_401_if_email_is_not_found(client):
    response = client.post("/api/auth/login", json={"email": "user_e@example.com", "password": "password_c"},)
    assert response.status_code == 401

def test_authernicate_user_generates_a_token_when_invoke_with_vaild_email_and_password(client):
    response = client.post("/api/auth/login", json={"email": "user_c@example.com", "password": "password_c"},)
    body = response.json()
    assert type(body['token']) == str

def test_register_user_responds_with_201_if_given_the_correct_fields(client):
    response = client.post("/api/auth/register", json={"name": "user_d", "email": "user_d@example.com", "password": "password_d"},)
    assert response.status_code == 201


def test_register_user_responds_with_400_if_missing_name(client):
    response = client.post("/api/auth/register", json={"email": "user_d@example.com", "password": "password_d"},)
    assert response.status_code == 400

def test_register_user_responds_with_400_if_missing_email(client):
    response = client.post("/api/auth/register", json={"name": "user_d", "password": "password_d"},)
    assert response.status_code == 400

def test_register_user_responds_with_400_if_missing_password(client):
    response = client.post("/api/auth/register", json={"name": "user_d", "email": "user_d@example.com"},)
    assert response.status_code == 400

def test_register_user_responds_with_409_if_email_is_already_registered(client):
    response = client.post("/api/auth/register", json={"name": "user_d", "email": "user_c@example.com", "password": "password_d"},)
    assert response.status_code == 409




