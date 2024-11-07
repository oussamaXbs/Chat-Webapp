from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, send, join_room, leave_room
import os
import json

# Initialize the Flask app and SocketIO
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

# File path for user data
USER_DATA_FILE = 'users.json'

# A function to load user data from the JSON file
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# A function to save user data to the JSON file
def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

# Load users when the app starts
users = load_users()

@app.route('/')
def signup():
    return render_template('SignupPage.html')  # Signup page

@app.route('/signup', methods=['POST'])  # Ensure this is POST
def signup_user():
    data = request.get_json()  # Expecting JSON data
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists'})

    users[username] = password
    save_users(users)  # Save the updated users data
    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        session['username'] = username
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'})

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('ChatPage.html', username=session['username'])
    return redirect(url_for('signup'))

# SocketIO event for real-time messaging
@socketio.on('message')
def handle_message(message):
    send(message, broadcast=True)

# SocketIO event for joining a room (chat room)
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f'{username} has entered the room.', room=room)

# SocketIO event for leaving a room
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f'{username} has left the room.', room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
