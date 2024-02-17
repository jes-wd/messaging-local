# server.py
import socket
import threading

# Server's IP address
# If the server is not on this machine, 
# set the SERVER variable to the external IP address of the server
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (SERVER, PORT)

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the address
server.bind(ADDR)

clients = []
nicknames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_client(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'), client)
            nicknames.remove(nickname)
            break

def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(f'Nickname of the client is {nickname}!')
        broadcast(f"{nickname} joined the chat!".encode('utf-8'), client)
        client.send('Connected to the server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    server.listen()
    print(f"Server listening on {SERVER}")
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    receive_thread.join()
    server.close()
