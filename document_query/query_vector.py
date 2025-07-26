import requests
import weaviate
from .base_query import Query
from config import Config

class WeaviateQuery(Query):
    def __init__(self, configur:Config):
        self.client =weaviate.connect_to_local()
        self.ollama_url = configur.OLLAMA_URL
        self.class_name = "HarryPotterGOF"
    
    def sayHello(self):
        return self.ollama_url," "

    def _get_embedding(self, query_text):
        response = requests.post(
            f"{self.ollama_url}/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": query_text}
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def query_similar_documents(self, query_text, top_k=5):
        # Get embedding for query
        query_embedding = self._get_embedding(query_text)

        # Get collection
        collection = self.client.collections.get(self.class_name)

        # Perform vector search
        results = collection.query.near_vector(
            near_vector=query_embedding,
            limit=top_k, # Optional: for similarity score
            return_properties=["text", "page_number"]
        )

        return results.objects



