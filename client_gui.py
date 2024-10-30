import tkinter as tk
import socket
import threading
import time
import os
from tkinter import messagebox 
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

window = tk.Tk()
window.resizable(False, False)
username = " "
window.title("Client")
#el frame 1(name and connect button)
topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Username:" ,font=('Tekton Pro',11))
lblName.pack(side=tk.LEFT,padx=(0,5))
entName = tk.Entry(topFrame, width=30,borderwidth=3)
entName.pack(side=tk.LEFT)
entName.bind("<Return>", (lambda event: connect()))
btnConnect = tk.Button(topFrame, text="Connect",font=('sans 11 bold') ,command=lambda : connect(), width=8, bd=4, fg='green')
btnConnect.pack(side=tk.LEFT, pady=(7,7),padx=(15,0))
topFrame.pack(side=tk.TOP,pady=(10,0))
#frame 2 (text and 2 display screens)
#screen 1
displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="messages",font=('Tekton Pro', 16)).pack(padx=(0,0))
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 10))
tkDisplay.tag_config("tag_your_message", foreground="blue")
tkDisplay.config(background="#F4F6F7", highlightbackground="grey", state="disabled",highlightthickness=2)
#screen2
#joined clients list display screen (canceled)

displayFrame.pack(side=tk.TOP)
#frame 3 (message zone and send button maybe)
bottomFrame = tk.Frame(window)

tkMessage = tk.Text(bottomFrame, height=1, width= 40,borderwidth=3)
tkMessage.pack(side=tk.LEFT,padx=(0,0),pady=(5,5))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))

btntext = tk.Button(bottomFrame, text="send msg",font=('sans 11 bold') , width=8, bd=4,command=lambda: getChatMessage(tkMessage.get("1.0", tk.END)))
btntext.pack(side=tk.RIGHT,pady=(5,5),padx=(20,0))
btntext.config(state=tk.DISABLED)
bottomFrame.pack(side=tk.TOP)

#frmae 4 (file sending frame)
bottomFrame2= tk.Frame(window)
fileLocation=tk.Label(bottomFrame2,text="choose file to send",width=33,bg = "#DBE1E3")
fileLocation.pack(side=tk.LEFT,padx=(0,0),pady=(5,7))

btnfileSend = tk.Button(bottomFrame2, text="send file",font=('sans 11 bold') , width=8, bd=4)
btnfileSend.pack(side=tk.RIGHT,padx=(0,0),pady=(5,7))
btnfileSend.config(state=tk.DISABLED)
btnfileBrowse = tk.Button(bottomFrame2, text="browse",font=('sans 11 bold') ,width=8, bd=4, command=lambda:browseFile())
btnfileBrowse.pack(side=tk.RIGHT,padx=(20,5),pady=(5,7))
btnfileBrowse.config(state=tk.DISABLED)
bottomFrame2.pack(side=tk.BOTTOM)


def connect():
    global username, client
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <ex. oussama>")
    else:
        username = entName.get()
        connect_to_server(username)

# the server
client = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 55555

import tkinter as tk
from tkinter import messagebox
import socket
import threading

def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR
    if not name:
        messagebox.showerror(title="ERROR", message="Username cannot be empty.")
        return

    try:
        # Initialize socket and connect to server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode())  # Send the username to the server

        # Update UI states after successful connection
        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        btntext.config(state=tk.NORMAL)
        btnfileSend.config(state=tk.NORMAL)
        btnfileBrowse.config(state=tk.NORMAL)
        tkMessage.config(state=tk.NORMAL)

        # Start a new thread to receive messages from the server
        threading.Thread(target=receive_message_from_server, args=(client, "m"), daemon=True).start()
    
    except Exception as e:
        messagebox.showerror(
            title="ERROR", 
            message=f"Cannot connect to host: {HOST_ADDR} on port: {HOST_PORT}. Server may be unavailable. Try again later."
        )

def receive_message_from_server(sck, m):
    while True:
        try:
            from_server = sck.recv(1024).decode()
            if not from_server:
                break

            # Display message from server in chat window
            texts = tkDisplay.get("1.0", tk.END).strip()
            tkDisplay.config(state=tk.NORMAL)

            # Display received message
            if len(texts) < 1:
                tkDisplay.insert(tk.END, from_server)
            else:
                tkDisplay.insert(tk.END, "\n\n" + from_server)

            tkDisplay.config(state=tk.DISABLED)
            tkDisplay.see(tk.END)

        except Exception as e:
            print(f"Error receiving message: {e}")
            break

    # Close socket and update UI on disconnect
    sck.close()
    messagebox.showinfo("Disconnected", "You have been disconnected from the server.")
    window.destroy()
    
def getChatMessage(msg):
    msg = msg.replace('\n', '').strip()  # Remove any newline and leading/trailing whitespace

    if not msg:
        return  # Avoid sending empty messages

    # Get current text in the display box and prepare to update it
    texts = tkDisplay.get("1.0", tk.END).strip()
    tkDisplay.config(state=tk.NORMAL)

    # Insert the message in the display box with custom tag
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message")
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

    # Lock the display box and scroll to the end
    tkDisplay.config(state=tk.DISABLED)
    tkDisplay.see(tk.END)

    # Attempt to send the message and clear the input if successful
    try:
        send_message_to_server(msg)
        tkMessage.delete('1.0', tk.END)  # Clear input only if sent successfully
    except Exception as e:
        print(f"Failed to send message: {e}")
        messagebox.showerror("Error", "Message failed to send.")


def send_message_to_server(msg):
    global client  # Ensures we modify the global client variable if needed

    try:
        # Convert the message to string and encode it
        client_msg = str(msg)
        client.send(client_msg.encode())

        # If the message is "exit," handle disconnection
        if msg == "exit":
            client.send("disconnecting".encode())
            window.after(100, lambda: client.close())  # Slight delay to ensure message reaches the server
            window.after(500, lambda: window.destroy())  # Close the GUI shortly after disconnecting

        print("Sending message:", msg)  # Optional: Print message for debugging
    except Exception as e:
        print("Error sending message:", e)
        messagebox.showerror("Error", "Failed to send message. Please check your connection.")

import os
from tkinter import filedialog

def browseFile():
    try:
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select a file",
            filetypes=(("Text files", "*.txt*"), ("All files", "*.*"))
        )
        
        if filename:
            # Display only the file name, not the full path
            fileLocation.configure(text="File Opened: " + os.path.basename(filename))
            
            # Optionally, return the filename for further processing
            return filename
        else:
            fileLocation.configure(text="No file selected")  # Message if no file is chosen
    except Exception as e:
        fileLocation.configure(text="Error opening file")
        print("Error:", e)

def on_closing():
    if client:
        print("Sending exit message to server.")
        client.send("exit".encode())  # Send exit message to server
        client.close()  # Close the socket connection
    window.destroy()  # Destroy the window

# Bind the window close event to the on_closing function
window.protocol("WM_DELETE_WINDOW", on_closing)


def sendFile_to_server(filename):
    try:
        # Check if file exists and get its size
        file_size = os.path.getsize(filename)
        
        # Send file size to server
        client.send(str(file_size).encode())
        print("Sending file...")

        # Open file in binary mode and send its content
        with open(filename, 'rb') as file:
            data = file.read()
            client.sendall(data)
        
        print("File sent successfully")
        
    except Exception as e:
        print("Error sending file:", e)
    
    
"""
def darktheme():
    window.config(background="black")
    entName.config(background="black")
    btnConnect.config(background="black")
    topFrame.config(background="black")
    displayFrame.config(background="black")
    bottomFrame.config(background="black")
    tkDisplay.config(background="black")
    tkDisplay2.config(background="black")
"""
    
# Setting icon of my window
p1 = PhotoImage(file = 'images.png')
window.iconphoto(False, p1)
# main window
window.mainloop()
