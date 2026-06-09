import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_analyze_word_count():
    response = client.post("/analyze", json={"text": "Hola mundo esta es una prueba"})
    assert response.status_code == 200
    assert response.json()["word_count"] == 6

def test_analyze_sentence_count():
    response = client.post("/analyze", json={"text": "Hola mundo. Como estas? Bien!"})
    assert response.status_code == 200
    assert response.json()["sentence_count"] == 3

def test_analyze_empty_text():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 200
    assert response.json()["word_count"] == 0

@pytest.mark.skipif(True, reason="requires local Ollama")
def test_evaluate_returns_response():
    response = client.post("/evaluate", json={"prompt": "Di solo la palabra: hola"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "word_count" in data
    assert "char_count" in data

@pytest.mark.skipif(True, reason="requires local Ollama")
def test_evaluate_response_not_empty():
    response = client.post("/evaluate", json={"prompt": "Di solo la palabra: hola"})
    assert response.status_code == 200
    assert len(response.json()["response"]) > 0

@pytest.mark.skipif(True, reason="requires local Ollama")
def test_evaluate_returns_prompt():
    response = client.post("/evaluate", json={"prompt": "Di solo la palabra: hola"})
    assert response.status_code == 200
    assert response.json()["prompt"] == "Di solo la palabra: hola"

@pytest.mark.skipif(True, reason="requires local Ollama")
def test_evaluate_has_quality_metrics():
    response = client.post("/evaluate", json={"prompt": "Di solo la palabra: hola"})
    assert response.status_code == 200
    data = response.json()
    assert "quality" in data
    assert "is_empty" in data["quality"]
    assert "is_too_short" in data["quality"]
    assert "language" in data["quality"]

@pytest.mark.skipif(True, reason="requires local Ollama")
def test_evaluate_not_empty():
    response = client.post("/evaluate", json={"prompt": "Di solo la palabra: hola"})
    assert response.status_code == 200
    assert response.json()["quality"]["is_empty"] == False