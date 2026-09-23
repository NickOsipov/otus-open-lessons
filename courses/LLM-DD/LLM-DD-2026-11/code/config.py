"""Module: config
Description: Константы Qdrant, эмбеддингов и локальной LLM в Ollama.
"""

import os

from dotenv import load_dotenv
from qdrant_client.http import models

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "orbit_knowledge"
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
VECTOR_SIZE = 384
DISTANCE = models.Distance.COSINE
SEARCH_LIMIT = 3
QUERY_TEXT = "как оформить возврат"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
