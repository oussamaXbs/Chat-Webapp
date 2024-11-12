const socket = new WebSocket('ws://localhost:3000');

const messages = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');

socket.onmessage = (event) => {
    const message = document.createElement('div');
    message.textContent = event.data;
    messages.appendChild(message);
};

sendBtn.addEventListener('click', () => {
    if (messageInput.value.trim()) {
        socket.send(messageInput.value);
        messageInput.value = '';
    }
});

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendBtn.click();
});
