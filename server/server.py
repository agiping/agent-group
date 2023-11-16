import socket
import threading

def handle_client(client_socket, client_address):
    while True:
        msg = client_socket.recv(1024).decode('utf-8')
        if msg:
            print(f"Message from {client_address}: {msg}")
            broadcast_message(msg, client_address)

def broadcast_message(message, sender_address):
    for client in clients:
        if client != sender_address:
            clients[client].sendall(message.encode('utf-8'))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 允许地址重用
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 54321))
    server_socket.listen()
    print("Server is running and listening for connections...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")
        clients[client_address] = client_socket
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

clients = {}
start_server()