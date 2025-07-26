import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_URL=os.getenv("OLLAMA_URL")
    WEAVIATE_URL=os.getenv("WEAVIATE_URL")
    SOURCE_FILE=os.getenv("SOURCE_FILE")
    OLLAMA_LLM=os.getenv("OLLAMA_LLM")
    OPENAI_KEY=os.getenv("OPENAI_API_KEY")
