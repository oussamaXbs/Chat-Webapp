import tkinter as tk
import socket
import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import font
window = tk.Tk()
window.title("ChatRomm Sever")
window.resizable(False, False)


# el frame 1 (2 buttons)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect",font=('Tekton Pro', 11), command=lambda : start_server(), width=8, bd=4, fg='green')
btnStart.pack(side=tk.LEFT,pady=(7,0))
btnStop = tk.Button(topFrame, text="Stop",font=('Tekton Pro', 11), command=lambda : stop_server(), width=8, bd=4, fg='red' , state=tk.DISABLED)
btnStop.pack(side=tk.LEFT, pady=(7,0), padx=(15,0))
topFrame.pack(side=tk.TOP, pady=(5, 0))

# el frame 2 (port and host)
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: unknown")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# el frame 3 (clients area)
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="********Client List********",font=('Tekton Pro', 16)).pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8000
client_name = " "
clients = []
clients_names = []


# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT
    try:
        # Disable the Start button and enable the Stop button
        btnStart.config(state=tk.DISABLED)
        btnStop.config(state=tk.NORMAL)

        # Set up and start the server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST_ADDR, HOST_PORT))
        server.listen(5)
        print("Server started on:", HOST_ADDR, "Port:", HOST_PORT)

        # Start a new thread to accept clients
        threading.Thread(target=accept_clients, args=(server,)).start()

        # Display the server address and port
        lblHost["text"] = "Host: " + HOST_ADDR
        lblPort["text"] = "Port: " + str(HOST_PORT)
        
    except Exception as e:
        print("Error starting server:", e)

# Stop server function
def stop_server():
    global server
    try:
        # Disable the Stop button and enable the Start button
        btnStart.config(state=tk.NORMAL)
        btnStop.config(state=tk.DISABLED)    

        # Close the server socket if it's open
        if server:
            server.close()
            print("Server stopped.")

        # Optional: Join any threads or perform cleanup here if needed
        # For example, if you have threads accepting clients, you might want to signal them to stop.
        
    except Exception as e:
        print("Error stopping the server:", e)


# tzid clients lel liste clients    
def accept_clients(the_server):
    try:
        while True:
            # Accept a new client connection
            client, addr = the_server.accept()
            print(f"Connection accepted from {addr}")
            clients.append(client)

            # Start a new thread to handle the client's messages
            threading.Thread(target=send_receive_client_message, args=(client, addr)).start()
    except Exception as e:
        print("Error accepting clients:", e)



#receive message from current client AND
# Send that message to other clients




def send_receive_client_message(client_connection, client_ip_addr):
    global server, clients, clients_names

    try:
        # Receive the client's name
        client_name = client_connection.recv(1024).decode()
        welcome_msg = f"Welcome {client_name}! Use 'exit' to quit the conversation."
        client_connection.send(welcome_msg.encode())

        # Add the new client to the lists
        clients.append(client_connection)
        clients_names.append(client_name)
        update_client_names_display(clients_names)  # Update the display for all clients

        # Notify other clients about the new connection
        for c in clients:
            if c != client_connection:
                add_msg = f"{client_name} joined the chat!!"
                c.send(add_msg.encode())

        while True:
            data = client_connection.recv(1024).decode()
            if not data:  # Client disconnected unexpectedly
                print(f"{client_name} disconnected unexpectedly.")
                break

            if data == "exit":  # Client sent exit command
                print(f"{client_name} has exited the chat.")
                break
            
            # Send received message to all other clients
            idx = clients.index(client_connection)  # Get index of the current client
            for c in clients:
                if c != client_connection:
                    server_msg = f"{client_name} -> {data}"
                    c.send(server_msg.encode())

    except Exception as e:
        print(f"Error while handling client {client_name}: {e}")

    finally:
        # Cleanup after disconnection
        try:
            idx = clients.index(client_connection)
            if idx != -1:
                client_name = clients_names[idx]
                del clients_names[idx]  # Remove the client's name
                del clients[idx]  # Remove the client's socket connection
                
                # Notify remaining clients
                for c in clients:
                    if c != client_connection:
                        add_msg = f"{client_name} left the chat!!"
                        c.send(add_msg.encode())
                
                update_client_names_display(clients_names)  # Update the client list display

            client_connection.close()  # Close the client connection

        except ValueError:
            # This error can occur if the client was not found in the list
            print(f"Client connection not found during cleanup for {client_name}.")



# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx

# mise a jour lel client names display wa9t client ya3ml connect OR
# wa9t client ya3ml disconnect 
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)

# el icon
p1 = PhotoImage(file = 'server.png')

# Setting icon of my window
window.iconphoto(False, p1)
# main window
window.mainloop()
