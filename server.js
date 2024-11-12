const express = require('express');
const { WebSocketServer } = require('ws');
const http = require('http');

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

app.use(express.static('public'));

// Function to broadcast messages to all clients except the sender
function broadcast(data, sender) {
    wss.clients.forEach((client) => {
        if (client !== sender && client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(data));
        }
    });
}

wss.on('connection', (ws) => {
    // Variable to store the username for each connection
    let username = '';

    // Listen for messages from the client
    ws.on('message', (data) => {
        const messageData = JSON.parse(data);

        if (messageData.type === 'join') {
            // Store the username and broadcast the join message
            username = messageData.username;
            const joinPayload = { type: 'notification', message: `${username} has joined the chat!` };
            broadcast(joinPayload, ws);
        } else if (messageData.type === 'message') {
            // Broadcast the user's chat message
            const payload = { type: 'message', username, message: messageData.message };
            broadcast(payload, ws);
        }
    });

    // Handle when a user disconnects
    ws.on('close', () => {
        if (username) {
            const leavePayload = { type: 'notification', message: `${username} has left the chat.` };
            broadcast(leavePayload, ws);
        }
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
