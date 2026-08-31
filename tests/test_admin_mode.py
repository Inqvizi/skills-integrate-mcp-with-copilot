import base64

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def _basic_auth(username: str, password: str):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def test_teacher_login_accepts_valid_credentials():
    response = client.post(
        "/auth/login",
        json={"username": "teacher1", "password": "password1"},
    )

    assert response.status_code == 200
    assert response.json()["authenticated"] is True


def test_teacher_login_rejects_invalid_credentials():
    response = client.post(
        "/auth/login",
        json={"username": "teacher1", "password": "wrong-password"},
    )

    assert response.status_code == 401


def test_activity_signup_requires_teacher_auth():
    response = client.post("/activities/Chess Club/signup?email=student@example.edu")

    assert response.status_code == 401


def test_teacher_can_sign_up_student():
    response = client.post(
        "/activities/Chess Club/signup?email=teacher-test@example.edu",
        headers=_basic_auth("teacher1", "password1"),
    )

    assert response.status_code == 200
    assert "teacher-test@example.edu" in response.json()["message"]
