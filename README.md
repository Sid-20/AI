
Installation:
-> Get all dependencies with requirements.txt
-> Must have a OpenAI API Key
-> Use Docker Desktop for Weaviate and Ollama installation


-------OLLAMA DOCKER COMMANDS----
docker stop ollama
docker start ollama

------WEAVIATE DOCKER COMMANDS-----
docker-compose up -d
docker-compose down


## 🚀 Features

- Upload PDF files and extract text
- Chunk PDF pages into smaller overlapping text chunks
- Generate vector embeddings (via Ollama nomic-embed-text)
- Store and query chunks in Weaviate
- Ask natural language questions and get relevant answers
- Clean and extendable backend structure
- Web frontend built with HTML + JS
