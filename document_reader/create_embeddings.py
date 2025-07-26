import fitz  # PyMuPDF
import requests
import weaviate
import hashlib
from uuid import uuid4
from config import Config
import weaviate.classes.config as wc
from weaviate.collections.filters import _FilterAnd

class WeaviateVector:
    def __init__(self, configur:Config):
        self.pdf_path = configur.SOURCE_FILE
        self.ollama_url = configur.OLLAMA_URL
        self.class_name = "HarryPotterGOF"
        self.file_id = "HarryPotter"

        self.client = weaviate.connect_to_local()
 

        # Create schema if not already
        self._create_schema()
    
    def sayHello(self):
        return self.pdf_path,self.ollama_url
    

    def _generate_file_id(self):
        with open(self.pdf_path, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        return file_hash
    
    def _create_schema(self):
        # Check if collection exists
        if not self.client.collections.exists(self.class_name):
            pdf_collection = self.client.collections.create(
            name=self.class_name,
            properties=[
                wc.Property(name="text", data_type=wc.DataType.TEXT),
                wc.Property(name="page_number", data_type=wc.DataType.INT),
                wc.Property(name="document_name", data_type=wc.DataType.TEXT),
            ],
            vectorizer_config=wc.Configure.Vectorizer.none(),  # Don't vectorize automaticall  Optional
            vector_index_config=wc.Configure.VectorIndex.hnsw(
                distance_metric=wc.VectorDistances.COSINE
            )
        )
        
            




    def _pdf_already_processed(self):
        query = (
            self.client.query
            .get(self.class_name, ["file_id"])
            .with_where({
                "path": ["file_id"],
                "operator": "Equal",
                "valueText": self.file_id
            })
        )
        result = query.do()
        return bool(result.get('data', {}).get('Get', {}).get(self.class_name))

    def _read_pdf(self):
        doc = fitz.open(self.pdf_path)
        for page_num in range(len(doc)):
            text = doc.load_page(page_num).get_text()
            yield page_num + 1, text
    

    def _get_embedding(self, text):
        response = requests.post(
            f"{self.ollama_url}/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]
    
    def clear_collection(self):
        
        if self.client.collections.exists(self.class_name):
            self.client.collections.delete(self.class_name)
        else:
            print(f"[i] Collection '{self.class_name}' does not exist.")
    
    def chunk_with_overlap(self,text, chunk_size=300, overlap=100):
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks


    
    def ingest_pdf(self):
        file_path = self.pdf_path
        collection = self.client.collections.get(self.class_name)
        document_name = file_path.split("/")[-1]

        for page_number, text in self._read_pdf():
            if not text.strip():
                continue

            chunks = self.chunk_with_overlap(text, chunk_size=500, overlap=100)

            for chunk_index, chunk in enumerate(chunks):
                embedding = self._get_embedding(chunk)
                print(f"Page {page_number}, Chunk {chunk_index + 1} created")

                collection.data.insert(
                    properties={
                        "text": chunk,
                        "page_number": page_number,
                        "chunk_index": chunk_index,
                        "document_name": document_name
                    },
                    vector=embedding
                )
        print("✅ PDF successfully chunked and ingested into Weaviate.")

    
    




