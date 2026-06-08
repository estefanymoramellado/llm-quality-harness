from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextRequest(BaseModel):
    text: str

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