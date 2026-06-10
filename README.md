# LLM Quality Harness

![CI](https://github.com/estefanymoramellado/llm-quality-harness/actions/workflows/ci.yml/badge.svg)

REST API para análisis de texto y evaluación automática de calidad de respuestas generadas por modelos de lenguaje (LLMs).

## ¿Por qué existe este proyecto?

Los LLMs no siempre responden bien. A veces dan respuestas vacías, demasiado cortas, en el idioma incorrecto, o sin coherencia con el prompt. Este proyecto nació para medir y detectar esos problemas automáticamente — incluyendo un sistema de evaluación con LLM-as-a-Judge y observabilidad completa con Langfuse.

## ¿Qué hace?

- Analiza métricas de texto: palabras, caracteres, oraciones
- Envía prompts a un LLM local (Ollama) y evalúa la respuesta
- Detecta el idioma de la respuesta y su nivel de confianza
- Flags automáticos si la respuesta está vacía o es demasiado corta
- **LLM-as-a-Judge**: usa el mismo modelo para evaluar la calidad de su propia respuesta con un score del 1 al 5 y feedback
- **Token tracking**: registra prompt_tokens, completion_tokens y total_tokens de cada llamada
- **Observabilidad con Langfuse**: cada evaluación queda registrada con latencia, métricas y tokens en un dashboard en tiempo real
- Suite de tests automatizados con pytest y CI/CD con GitHub Actions

## Tecnologías

- Python 3.14
- FastAPI
- pytest
- Ollama + Qwen 2.5 Coder 7B (LLM local)
- Langfuse (observabilidad)
- GitHub Actions (CI/CD)

## Requisitos previos

Este proyecto requiere [Ollama](https://ollama.com) corriendo localmente con el modelo Qwen 2.5 Coder.

1. Instala Ollama desde https://ollama.com
2. Descarga el modelo:
```bash
ollama pull qwen2.5-coder:7b
```
3. Verifica que Ollama está corriendo:
```bash
ollama serve
```

## Instalación

```bash
git clone https://github.com/estefanymoramellado/llm-quality-harness.git
cd llm-quality-harness
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con tus credenciales de Langfuse:

LANGFUSE_SECRET_KEY=tu_secret_key
LANGFUSE_PUBLIC_KEY=tu_public_key
LANGFUSE_HOST=https://cloud.langfuse.com

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
| POST | `/evaluate` | Envía prompt a LLM y evalúa la respuesta con LLM-as-a-Judge |

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
    "language_confidence": "high",
    "judge_score": 4,
    "judge_feedback": "Respuesta clara y concisa, cubre el concepto principal.",
    "prompt_tokens": 42,
    "completion_tokens": 38,
    "total_tokens": 80
  }
}
```

## Observabilidad

Cada llamada al endpoint `/evaluate` queda registrada automáticamente en Langfuse con:
- Latencia total de la evaluación
- Input y output completos
- Métricas de calidad
- Score del juez
- Consumo de tokens

## Limitaciones conocidas

- El juez usa el mismo modelo que genera la respuesta — puede ser condescendiente consigo mismo
- La detección de idioma tiene baja confianza con textos menores a 3 palabras
- Los tests de Ollama se saltan en CI/CD por requerir entorno local
- El token tracking depende de los campos `prompt_eval_count` y `eval_count` de Ollama