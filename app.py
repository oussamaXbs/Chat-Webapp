from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import SocketIO, send, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app, SocketIO, and SQLAlchemy
app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

# Define the User model (database table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create the database tables (if not already created)
with app.app_context():
    db.create_all()

@app.route('/')
def signup():
    return render_template('SignupPage.html')  # Signup page

@app.route('/signup', methods=['POST'])
def signup_user():
    data = request.get_json()  # Expecting JSON data from frontend
    username = data.get('username')
    password = data.get('password')

    # Check if username already exists in the database
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'Username already exists'})

    # Create new user and add to the database
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if user exists and the password matches
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session['username'] = username  # Store username in session
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
