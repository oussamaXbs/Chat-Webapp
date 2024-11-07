from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Store messages in memory
messages = []

@app.route('/')
def index():
    return render_template('username.html')

@socketio.on('send_message')
def handle_send_message(data):
    msg = data['message']
    messages.append(msg)  # Add message to the list
    emit('receive_message', {'messages': messages}, broadcast=True)  # Broadcast all messages to all clients

@socketio.on('get_messages')
def handle_get_messages():
    emit('receive_message', {'messages': messages})  # Send all messages to the client

@socketio.on('reset_chat')
def handle_reset_chat():
    global messages
    messages = []  # Clear the chat history
    emit('receive_message', {'messages': messages}, broadcast=True)  # Notify all clients of reset

if __name__ == '__main__':
    socketio.run(app, debug=True)