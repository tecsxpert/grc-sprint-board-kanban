from unittest.mock import patch

import pytest

from app import create_app
from services.groq_client import GroqClient


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_describe_success_with_mocked_ai(client, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    with patch.object(GroqClient, "_post_completion", return_value={"choices": [{"message": {"content": "Summary: done"}}]}):
        response = client.post("/describe", json={"task_title": "Create API"})
    assert response.status_code == 200
    assert response.json["success"] is True


def test_generate_report_requires_sprint_name(client):
    response = client.post("/generate-report", json={"completed_tasks": 1, "total_tasks": 2})
    assert response.status_code == 400


def test_recommend_requires_tasks(client):
    response = client.post("/recommend", json={"tasks": []})
    assert response.status_code == 400
