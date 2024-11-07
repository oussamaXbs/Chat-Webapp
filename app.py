from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Store messages in memory for simplicity
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    msg = request.form['message']
    messages.append(msg)  # Add message to the list
    return jsonify({'status': 'success'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    global messages
    messages = []  # Clear the chat history
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
