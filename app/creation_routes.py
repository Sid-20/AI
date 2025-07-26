# app/routes.py

from flask import Blueprint, request, jsonify, current_app, render_template

# Create the Blueprint
bp = Blueprint('main_bp', __name__)

# Add a route
@bp.route("/start", methods=["GET"])
def ping():
    return jsonify({"message": "App initiated!"})


@bp.route("/potterPDF", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/check_objects",methods=["GET"])
def check_objects():
    source_file,ollama_url=current_app.extensions["weaviatevector"].sayHello()
    return jsonify({"source_file": source_file,"ollama_url":ollama_url})

@bp.route("/empty_db",methods=["POST"])
def delete_objects():
    current_app.extensions["weaviatevector"].clear_collection()
    return jsonify({"message": "deletd successfully","ollama_url":"used"})


# Add a route that uses your vector class
@bp.route("/create_embeddings", methods=["POST"])
def embed_pdf():
    weaviatevector = current_app.extensions["weaviatevector"]
    weaviatevector.ingest_pdf()
    # You can now use methods on your WeaviateVector instance
    return jsonify({"message": "Embedding complete"})
