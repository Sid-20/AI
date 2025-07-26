from config import Config
import requests

class Ollama:

    def __init__(self,configur:Config):
        self.ollama_url=configur.OLLAMA_URL
        self.model_name=configur.OLLAMA_LLM

    def _build_prompt(self, context: str, question: str) -> str:
        return f"""You are a helpful assistant. Answer the question to the user based on the context below.
        If the answer is not in the context, say "I couldn't find that information in the provided content.
        Form the most concluded answer on the given context"

        Context:
        {context}

        Question:
        {question}

        Answer:"""

    def get_answer(self, question: str, context) -> str:
        prompt = self._build_prompt(context, question)
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json().get("response", "No response from LLM.")
        except requests.RequestException as e:
            return f"Error contacting Ollama: {e}"