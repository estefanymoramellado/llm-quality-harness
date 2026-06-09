from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from langdetect import detect

app = FastAPI()

class TextRequest(BaseModel):
    text: str

class LLMRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "ok", "project": "llm-quality-harness"}

@app.post("/analyze")
def analyze_text(request: TextRequest):
    text = request.text
    words = text.split()
    
    return {
        "word_count": len(words),
        "char_count": len(text),
        "char_no_spaces": len(text.replace(" ", "")),
        "sentence_count": text.count(".") + text.count("!") + text.count("?"),
    }

@app.post("/evaluate")
def evaluate_llm(request: LLMRequest):
    response = httpx.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5-coder:7b",
            "prompt": request.prompt,
            "stream": False
        },
        timeout=120.0
    )
    
    llm_response = response.json()["response"]
    words = llm_response.split()
    word_count = len(words)

    try:
        language = detect(llm_response)
    except:
        language = "unknown"

    quality = {
        "is_empty": len(llm_response.strip()) == 0,
        "is_too_short": word_count < 10,
        "language": language,
        "language_confidence": "low" if word_count < 3 else "high"
    }

    return {
        "prompt": request.prompt,
        "response": llm_response,
        "word_count": word_count,
        "char_count": len(llm_response),
        "quality": quality
    }