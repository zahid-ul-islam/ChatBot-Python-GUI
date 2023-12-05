import socket
import threading

HOST = '127.0.0.1'
PORT = 5556

clients = []
lock = threading.Lock()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

def handle_client(client_socket, addr):
    with lock:
        clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            broadcast(message, client_socket)
        except:
            remove_client(client_socket)
            break

def broadcast(message, sender_socket):
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    remove_client(client)

def remove_client(client_socket):
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
            client_socket.close()

def start_server():
    print(f"Server is listening on {HOST}:{PORT}")
    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
