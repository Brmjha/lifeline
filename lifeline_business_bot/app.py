from flask import Flask, request, jsonify
import lifelinebot  

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    response = lifelinebot.handle_query(query)
    
    return jsonify({"response": response}), 200

@app.route('/chat', methods=['GET'])
def chat_get():
    message = request.args.get('message')
    # apikey = request.args.get('apikey')
    # You can use the apikey for authentication or other purposes
    # For now, we will just check if it's provided
    if not message:
    # or not apikey:
        return jsonify({"error": "Missing message"}), 400
    # Assuming your handle_query function can process the message
    response = lifelinebot.handle_query(message)

    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(debug=True)