# client.py
import socket
import threading

# Server's IP address
# If the server is running on the same machine as the client,
# you can use localhost or 127.0.0.1
# If the server is running on a different machine,
# replace 'localhost' with the IP address of the server
SERVER = "localhost"
PORT = 12345
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    while True:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == 'NICK':
                client.send(input("Choose a nickname: ").encode(FORMAT))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{input("")}'
        client.send(message.encode(FORMAT))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
