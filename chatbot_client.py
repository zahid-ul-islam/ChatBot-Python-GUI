import socket
import threading
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, END, StringVar, OptionMenu, Toplevel

class ChatClientManager:
    def __init__(self, master, client_name):
        self.master = master
        self.master.title(f"Chat Client - {client_name}")
        self.master.geometry("400x500")

        self.target_client_var = StringVar()
        self.target_client_var.set("All Clients")

        self.chat_display = Text(self.master, wrap="word", state="disabled")
        self.chat_display.pack(expand=True, fill="both")

        self.scrollbar = Scrollbar(self.master, command=self.chat_display.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_display["yscrollcommand"] = self.scrollbar.set

        self.target_menu = OptionMenu(self.master, self.target_client_var, "All Clients", "Client 1", "Client 2", "Client 3")
        self.target_menu.pack()

        self.input_entry = Entry(self.master, width=40)
        self.input_entry.pack(pady=10)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 5556))

        self.client_name = client_name

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self):
        target_client = self.target_client_var.get()
        user_input = self.input_entry.get()
        self.input_entry.delete(0, END)

        if target_client == "All Clients":
            message = f"{self.client_name} (to All): {user_input}"
        else:
            message = f"{self.client_name} (to {target_client}): {user_input}"

        self.client_socket.send(message.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.display_message(message)
            except:
                break

    def display_message(self, message):
        self.chat_display["state"] = "normal"
        self.chat_display.insert("end", message + "\n")
        self.chat_display["state"] = "disabled"
        self.chat_display.see("end")

class ChatClientApp:
    def __init__(self):
        self.root = tk.Tk()
        self.client1 = ChatClientManager(self.root, "Server")

        self.root2 = Toplevel(self.root)
        self.client2 = ChatClientManager(self.root2, "Riaz")

        self.root3 = Toplevel(self.root)
        self.client3 = ChatClientManager(self.root3, "Urmila")

        self.root.mainloop()

if __name__ == "__main__":
    ChatClientApp()
