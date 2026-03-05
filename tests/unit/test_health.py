"""Tests for health endpoint."""

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_healthy(client: TestClient) -> None:
    response = client.get("/health")
    assert response.json() == {"status": "healthy"}
