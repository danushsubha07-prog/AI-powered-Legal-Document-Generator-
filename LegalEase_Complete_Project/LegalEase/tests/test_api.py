from fastapi.testclient import TestClient

from legalese_api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "LegalEase" in response.json()["message"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_demo_mode():
    response = client.post(
        "/generate",
        json={
            "document_type": "Freelance Work Contract",
            "parties": "Jane Doe (Freelancer), TechNova Inc. (Client)",
            "terms": "Payment within 30 days; Confidentiality must be maintained",
            "dates": "September 27, 2026",
            "jurisdiction": "India",
            "language": "English",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "document" in data
    assert "FREELANCE WORK CONTRACT" in data["document"]


def test_generate_validation():
    response = client.post("/generate", json={"document_type": "x"})
    assert response.status_code == 422
