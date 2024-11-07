from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, send, join_room, leave_room
import os
import json

# Initialize the Flask app and SocketIO
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

# A simple in-memory database (dictionary) to store user credentials
users = {}

@app.route('/')
def signup():
    # Open the signup page first when the user visits the root
    return render_template('SignUpPage.html')

@app.route('/signup', methods=['POST'])
def signup_user():
    # Handle the signup logic (POST request)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists'})

    # Store the new user's data (in a real app, hash the password before storing it)
    users[username] = password
    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def user_login():
    # Handle login logic (POST request)
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
    # Ensure the user is logged in before showing the chat page
    if 'username' in session:
        return render_template('ChatPage.html', username=session['username'])
    return redirect(url_for('signup'))  # Redirect to the signup page if not logged in

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
