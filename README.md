# LLM Quality Harness

![CI](https://github.com/estefanymoramellado/llm-quality-harness/actions/workflows/ci.yml/badge.svg)

REST API para análisis de texto y evaluación automática de calidad de respuestas generadas por modelos de lenguaje (LLMs).

## ¿Por qué existe este proyecto?

Los LLMs no siempre responden bien. A veces dan respuestas vacías, demasiado cortas, en el idioma incorrecto, o sin coherencia con el prompt. Este proyecto nació para medir y detectar esos problemas automáticamente.

## ¿Qué hace?

- Analiza métricas de texto: palabras, caracteres, oraciones
- Envía prompts a un LLM local (Ollama) y evalúa la respuesta
- Detecta el idioma de la respuesta y su nivel de confianza
- Flags automáticos si la respuesta está vacía o es demasiado corta
- Suite de tests automatizados con pytest y CI/CD con GitHub Actions

## Tecnologías

- Python 3.14
- FastAPI
- pytest
- Ollama + Qwen 2.5 Coder 7B (LLM local)
- GitHub Actions (CI/CD)

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
| POST | `/evaluate` | Envía prompt a LLM y evalúa la respuesta |

## Ejemplo de respuesta del /evaluate

```json
{
  "prompt": "Explica qué es una API en una sola oración",
  "response": "Una API es un conjunto de reglas que permite que diferentes programas se comuniquen entre sí.",
  "word_count": 17,
  "char_count": 91,
  "quality": {
    "is_empty": false,
    "is_too_short": false,
    "language": "es",
    "language_confidence": "high"
  }
}
```