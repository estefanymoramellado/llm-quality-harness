import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from langdetect import detect
from langfuse import observe, get_client

load_dotenv()

langfuse = get_client()

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

def judge_response(prompt: str, response: str) -> dict:
    judge_prompt = f"""Eres un evaluador experto de respuestas de IA.

Dado este prompt: "{prompt}"
Y esta respuesta: "{response}"

Evalúa la calidad de la respuesta considerando:
- Relevancia con el prompt
- Claridad y coherencia
- Completitud

Responde ÚNICAMENTE con este JSON sin texto adicional:
{{"score": <número del 1 al 5>, "feedback": "<una oración breve>"}}"""

    try:
        judge_result = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:7b",
                "prompt": judge_prompt,
                "stream": False
            },
            timeout=120.0
        )
        raw = judge_result.json()["response"].strip()
        parsed = json.loads(raw)
        return {
            "judge_score": parsed.get("score"),
            "judge_feedback": parsed.get("feedback")
        }
    except:
        return {
            "judge_score": None,
            "judge_feedback": "Judge evaluation failed"
        }

@app.post("/evaluate")
@observe(name="evaluate")
def evaluate_llm(request: LLMRequest):
    try:
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:7b",
                "prompt": request.prompt,
                "stream": False
            },
            timeout=120.0
        )
        response.raise_for_status()
        ollama_data = response.json()
        prompt_tokens = ollama_data.get("prompt_eval_count", 0)
        completion_tokens = ollama_data.get("eval_count", 0)
    except httpx.ConnectError:
        return {"error": "LLM service unavailable. Make sure Ollama is running."}
    except httpx.TimeoutException:
        return {"error": "LLM service timed out. Try again or use a shorter prompt."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    llm_response = ollama_data["response"]
    words = llm_response.split()
    word_count = len(words)

    try:
        language = detect(llm_response)
    except:
        language = "unknown"

    judge = judge_response(request.prompt, llm_response)

    quality = {
        "is_empty": len(llm_response.strip()) == 0,
        "is_too_short": word_count < 10,
        "language": language,
        "language_confidence": "low" if word_count < 3 else "high",
        "judge_score": judge["judge_score"],
        "judge_feedback": judge["judge_feedback"],
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens
    }

    return {
        "prompt": request.prompt,
        "response": llm_response,
        "word_count": word_count,
        "char_count": len(llm_response),
        "quality": quality
    }