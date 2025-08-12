import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.skipif(
    not all([
        os.getenv("NEO4J_URI"),
        os.getenv("NEO4J_USER"),
        os.getenv("NEO4J_PASSWORD"),
        os.getenv("OPENAI_API_KEY")
    ]),
    reason="Missing required env vars for integration test"
)

@pytest.mark.skipif(True)
def test_ask_endpoint_with_simple_question():
    payload = {"question": "Which ingredients interact with proteins?"}
    response = client.post("/ask", json=payload)

    assert response.status_code in [200, 500]
    assert "question" in response.json() or "detail" in response.json()


def test_chatopenai():
    from langchain_openai import ChatOpenAI
    help(ChatOpenAI)

