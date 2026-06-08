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