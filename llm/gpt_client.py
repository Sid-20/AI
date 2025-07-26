from openai import OpenAI
import os

class GPTClient:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """
        Initializes the GPTClient with an optional API key and model name.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.model = model
        self.client=OpenAI(api_key=self.api_key)
        #openai.api_key = self.api_key

    def get_response(self, context: str, user_question: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a chatbot assistant.Summarize the context to answer the user question. Answer like you know the whole PDF "},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_question}"}
                ],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Error while generating response: {e}"
