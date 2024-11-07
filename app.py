from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Store messages in memory
messages = []
USER_DATA_FILE = 'users.json'

# Function to load users from the JSON file
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save users to the JSON file
def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file)

@app.route('/')
def index():
    return render_template('LoginPage.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('ChatPage.html', username=session['username'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Load existing users
        users = load_users()

        # Check if username exists
        if username in users:
            return "Username already exists. Please choose a different one.", 400

        # Hash the password and store the user
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        save_users(users)

        return redirect(url_for('index'))  # Redirect to login page after successful signup

    return render_template('SignupPage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Load users from file
        users = load_users()

        if username in users and check_password_hash(users[username], password):
            session['username'] = username  # Store username in session
            return redirect(url_for('chat'))
        else:
            return "Invalid username or password. Please try again.", 400

    return render_template('LoginPage.html')

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
