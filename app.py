from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a strong secret key for session management
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

messages = []  # Store messages in memory

@app.route('/')
def login():
    if 'username' in session:
        print("User already logged in. Redirecting to chat.")
        return redirect(url_for('chat'))
    print("Rendering login page.")
    return render_template('login.html')

@app.route('/set_username', methods=['POST'])
def set_username():
    username = request.form['username']
    if username:
        session['username'] = username
        print(f"Username set to {username}. Redirecting to chat.")
        return redirect(url_for('chat'))
    print("No username provided, redirecting back to login.")
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    if 'username' not in session:
        print("Username not found in session. Redirecting to login.")
        return redirect(url_for('login'))
    print("Rendering chat page.")
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' in session:
        msg = f"{session['username']}: {request.form['message']}"
        messages.append(msg)
        print(f"Message received: {msg}")
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Not logged in'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    global messages
    messages = []
    return jsonify({'status': 'success'})

@app.route('/logout')
def logout():
    session.pop('username', None)
    print("User logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
