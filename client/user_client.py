import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print("An error occurred:", e)
            client_socket.close()
            break

def main():
    host = 'localhost'
    port = 54321

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server.")

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input()
        if message == 'QUIT':
            client_socket.close()
            break
        client_socket.sendall(message.encode('utf-8'))

if __name__ == "__main__":
    main()
