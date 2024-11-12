let socket;
const loginContainer = document.getElementById('login-container');
const chatContainer = document.getElementById('chat-container');
const messages = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const usernameInput = document.getElementById('username-input');
const loginBtn = document.getElementById('login-btn');
let username = '';

// Handle Login Button Click
loginBtn.addEventListener('click', () => {
    username = usernameInput.value.trim(); // Get the username from input
    if (username) {
        // Store the username in session storage
        sessionStorage.setItem('username', username);

        // Hide the login container and show the chat container
        loginContainer.style.display = 'none';
        chatContainer.style.display = 'block';

        // Connect to WebSocket after setting the username
        connectWebSocket();
    } else {
        alert("Please enter a username to join the chat.");
    }
});

function connectWebSocket() {
    // Open a new WebSocket connection
    socket = new WebSocket('chat-web-app-h4ggd6h6hdh8cxec.canadacentral-01.azurewebsites.net');

    socket.onopen = () => {
        // Send a "join" event to the server with the username
        socket.send(JSON.stringify({ type: 'join', username }));
    };

    socket.onmessage = (event) => {
        const messageData = JSON.parse(event.data);
        
        const messageElement = document.createElement('div');
        if (messageData.type === 'message') {
            messageElement.textContent = `${messageData.username}: ${messageData.message}`;
        } else if (messageData.type === 'notification') {
            messageElement.textContent = messageData.message;
            messageElement.style.fontStyle = 'italic';  // Style for join/leave notifications
        }
        messages.appendChild(messageElement);
    };

    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
}

function sendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        // Display the message locally for the sender
        const messageElement = document.createElement('div');
        messageElement.textContent = `You: ${message}`;
        messageElement.style.fontWeight = 'bold';
        messages.appendChild(messageElement);

        // Send the message to the server
        socket.send(JSON.stringify({ type: 'message', username, message }));

        // Clear the input after sending
        messageInput.value = '';
    }
}

