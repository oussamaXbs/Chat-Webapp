from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Store messages in memory
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_send_message(data):
    msg = data['message']
    messages.append(msg)  # Add message to the list
    emit('new_message', {'message': msg}, broadcast=True)  # Broadcast message to all clients

@socketio.on('get_messages')
def handle_get_messages():
    emit('all_messages', messages)  # Send all messages to the client

@socketio.on('reset_chat')
def handle_reset_chat():
    global messages
    messages = []  # Clear the chat history
    emit('chat_reset', broadcast=True)  # Notify all clients of reset

if __name__ == '__main__':
    socketio.run(app, debug=True)
