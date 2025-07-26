# app/routes.py

from flask import Blueprint, request, jsonify, current_app, render_template

# Create the Blueprint
qr = Blueprint('main_qr', __name__)


@qr.route("/check_objects",methods=["GET"])
def check_objects():
    ollama_url,_=current_app.extensions["weaviatequery"].sayHello()
    return jsonify({"source_file": _,"ollama_url":ollama_url})

def extract_text_messages(weaviate_results):
    messages = []

    for obj in weaviate_results:
        text = obj.properties.get("text", "")
        if text:
            messages.append(text.strip())  # Clean and add text
    
    print(f"----Weaviate Results-----{messages}")

    return messages

# Add a route that uses your vector class
@qr.route("/ask", methods=["POST"])
def ask_query():
    data = request.get_json()
    query = data.get("question", "")
    print(f"------Query from User------{query}")
    weaviatequery = current_app.extensions["weaviatequery"]
    result=weaviatequery.query_similar_documents(query)
    messages=extract_text_messages(result)
    #ollama_llm=current_app.extensions["ollama_llm"]
    gpt_client=current_app.extensions["gpt_client"]
    print(f"-----Weaviate Result-----{messages}")
    answer=gpt_client.get_response(context=messages,user_question=query)


    # You can now use methods on your WeaviateVector instance
    #return jsonify({"result": final_resp})
    return jsonify({"answer": answer})
