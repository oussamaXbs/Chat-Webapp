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
HOST_ADDR = "127.0.0.1"
HOST_PORT = 55555
client_name = " "
clients = []
clients_names = []


# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT
    btnStart.config(state=tk.DISABLED,)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)    
    window.destroy()


# tzid clients lel liste clients    
def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append(client)
        threading._start_new_thread(send_receive_client_message, (client, addr))


#receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = ""

    # send welcome message to client
    client_name  = client_connection.recv(1024).decode()
    welcome_msg = "Welcome " + client_name + "!. Use 'exit' to quit conversation"
    client_connection.send(welcome_msg.encode())
    clients_names.append(client_name)
    update_client_names_display(clients_names)  #mise a jour lel client names
    for c in clients:
        if c!= client_connection:
            add_msg=f"{client_name} joined the chat!!"
            c.send(add_msg.encode())
    while True:
        data = client_connection.recv(1024).decode()
        if not data: break
        if data == "exit": break
        client_msg = data
        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_names[idx]

        for c in clients:
            if c != client_connection:
                server_msg = str(sending_client_name + "->" + client_msg)
                c.send(server_msg.encode())

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    client_name  = clients_names[idx]
    del clients_names[idx]
    del clients[idx]
    server_msg = "BYE "+client_name+"!"
    for c in clients:
        if c!= client_connection:
            add_msg=f"{client_name} left the chat!!"
            c.send(add_msg.encode())
    client_connection.send(server_msg.encode())
    client_connection.close()

    update_client_names_display(clients_names)  # mise a jour lel client names display




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
