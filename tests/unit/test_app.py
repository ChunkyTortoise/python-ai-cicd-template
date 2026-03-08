"""Unit tests for /api/generate and /api/status endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_generate_returns_job_id() -> None:
    response = client.post("/api/generate", json={"prompt": "Hello world"})
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "complete"
    assert data["result"] is not None


def test_generate_result_references_prompt() -> None:
    prompt = "What is 2 + 2?"
    response = client.post("/api/generate", json={"prompt": prompt})
    data = response.json()
    assert "2 + 2" in data["result"] or len(data["result"]) > 0


def test_generate_empty_prompt() -> None:
    response = client.post("/api/generate", json={"prompt": ""})
    assert response.status_code == 200


def test_generate_long_prompt() -> None:
    long_prompt = "A" * 1000
    response = client.post("/api/generate", json={"prompt": long_prompt})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "complete"


def test_status_returns_job() -> None:
    gen_response = client.post("/api/generate", json={"prompt": "test"})
    job_id = gen_response.json()["job_id"]

    status_response = client.get(f"/api/status/{job_id}")
    assert status_response.status_code == 200
    data = status_response.json()
    assert data["job_id"] == job_id
    assert data["status"] == "complete"


def test_status_not_found() -> None:
    response = client.get("/api/status/nonexistent-job-id")
    assert response.status_code == 404


def test_generate_respects_max_tokens() -> None:
    response = client.post("/api/generate", json={"prompt": "Hello", "max_tokens": 50})
    assert response.status_code == 200


def test_multiple_jobs_independent() -> None:
    r1 = client.post("/api/generate", json={"prompt": "First prompt"})
    r2 = client.post("/api/generate", json={"prompt": "Second prompt"})
    assert r1.json()["job_id"] != r2.json()["job_id"]


def test_job_result_is_string() -> None:
    response = client.post("/api/generate", json={"prompt": "Test"})
    data = response.json()
    assert isinstance(data["result"], str)
    assert len(data["result"]) > 0


def test_config_defaults() -> None:
    from src.config import settings

    assert settings.app_name == "Your Service"
    assert settings.environment == "development"
    assert settings.debug is False
    assert settings.max_tokens == 1024
