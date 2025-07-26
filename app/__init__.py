from flask import Flask
from config import Config
from document_reader.create_embeddings import WeaviateVector
from document_query.query_vector import WeaviateQuery
from llm.gpt_client import GPTClient
import os


def create_app():
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    templates_path = os.path.join(base_dir, "templates")
    app = Flask(__name__,template_folder=templates_path)
    
    # Load configuration
    #app.config.from_object("config.Config")  # Optional if you have a separate config.py

    weaviatevector=WeaviateVector(Config)

    weaviatequery=WeaviateQuery(Config)

    gpt_client=GPTClient(api_key=Config.OPENAI_KEY)

    #ollama_llm=Ollama(Config)

    app.extensions = getattr(app, 'extensions', {})
    app.extensions['weaviatevector'] = weaviatevector
    app.extensions['weaviatequery']= weaviatequery
    #app.extensions['ollama_llm']= ollama_llm
    app.extensions['gpt_client']= gpt_client

    from app.creation_routes import bp as main_bp
    from app.query_routes import qr as main_qr
    app.register_blueprint(main_bp,url_prefix="/creation")
    app.register_blueprint(main_qr,url_prefix="/query")



    return app
