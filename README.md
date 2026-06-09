# LLM Quality Harness

![CI](https://github.com/estefanymoramellado/llm-quality-harness/actions/workflows/ci.yml/badge.svg)

REST API para análisis de texto y evaluación de calidad de respuestas de modelos de lenguaje (LLMs).

## ¿Qué hace este proyecto?

- Analiza métricas de texto: palabras, caracteres, oraciones
- Evalúa la calidad de respuestas generadas por LLMs locales (Ollama)
- Suite de tests automatizados con pytest

## Tecnologías

- Python 3.14
- FastAPI
- pytest
- Ollama (LLM local)

## Instalación

```bash
git clone https://github.com/estefanymoramellado/llm-quality-harness.git
cd llm-quality-harness
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Correr el servidor

```bash
python -m uvicorn app.main:app --reload
```

## Correr los tests

```bash
python -m pytest tests/ -v
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/analyze` | Analiza métricas de un texto |