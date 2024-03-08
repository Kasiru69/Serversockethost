
import socket
import threading
import os

clients=set()
clients_lock=threading.Lock()
def handle_client(client_socket, addr,player):
    print(f"Accepted connection from {addr}{player}")

    while True:
        data = client_socket.recv(1030)
        if not data:
            break
        print(f"Received message from {addr}: {data}")
        with clients_lock:
            for _ in clients:
                _.sendall(f"Received message from {addr}: {data}".encode())

    client_socket.close()
    print(f"Connection from {addr} closed")

host='serversockethost-2.onrender.com'
port = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)

print(f"Server listening on {host}:{port}")
player=0
while True:
    client_socket, addr = server_socket.accept()
    print(client_socket)
    with clients_lock:
        clients.add(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr,player))
    client_thread.start()
    player+=1

