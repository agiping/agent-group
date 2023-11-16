import socket
import threading
import requests
from openai import OpenAI

DataAnalysis = "You are an advanced programmer, skilled in implementing complex applications with clean code"
Blogger = "You are a top blogger in platforms like meduim and infoQ."
DefaultRole = "You are a kind AI"

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print("Received:", message)
                if message.startswith("@DataAnalysis"):
                    role_content = DataAnalysis
                    message = message[len("@DataAnalysis"):]
                elif message.startswith("@Blogger"):
                    role_content = Blogger
                    message = message[len("@Blogger"):]
                else:
                    role_content = DefaultRole
                # 假设所有消息都是指令
                response = call_gpt_api(message, role_content)
                if response:
                    client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print("An error occurred:", e)
            client_socket.close()
            break

def call_gpt_api(prompt, rc):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": rc},
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message.content.strip()

def main():
    host = 'localhost'
    port = 54321

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("AI Client connected to the server.")

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

if __name__ == "__main__":
    main()
