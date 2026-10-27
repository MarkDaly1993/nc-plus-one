import pytest
from main import app
from fastapi.testclient import TestClient
from db.test_setup_files.connection_test import get_connection_to_database_test
from db.test_setup_files.test_seed import seed


@pytest.fixture(autouse=True)
def seed_test_db():
    connection = get_connection_to_database_test()
    seed(connection)

@pytest.fixture()
def client():
    return TestClient(app)


def test_authernicate_user_responds_with200(client):
    response = client.post("/api/auth/login", json{})
    assert response.status_code == 200