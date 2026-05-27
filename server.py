import socket
import threading
import os

# =========================
# SERVER CONFIG
# =========================

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 5555))

# =========================
# CREATE SOCKET
# =========================

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()

print(f"[SERVER STARTED] Running on port {PORT}")

# =========================
# CLIENT STORAGE
# =========================

clients = []
usernames = {}

# =========================
# BROADCAST FUNCTION
# =========================

def broadcast(message, sender=None):

    for client in clients:

        if client != sender:

            try:
                client.send(message)

            except:
                remove_client(client)

# =========================
# REMOVE CLIENT
# =========================

def remove_client(client):

    if client in clients:

        username = usernames.get(client, "Unknown")

        print(f"[DISCONNECTED] {username}")

        clients.remove(client)

        del usernames[client]

        client.close()

        broadcast(
            f"{username} left the virtual LAN.".encode()
        )

# =========================
# HANDLE CLIENT
# =========================

def handle_client(client):

    while True:

        try:
            message = client.recv(1024)

            if not message:
                break

            decoded = message.decode()

            print(decoded)

            broadcast(message, client)

        except:
            break

    remove_client(client)

# =========================
# ACCEPT CLIENTS
# =========================

while True:

    client, address = server.accept()

    print(f"[CONNECTED] {address}")

    # Ask username
    client.send("USERNAME".encode())

    username = client.recv(1024).decode()

    usernames[client] = username

    clients.append(client)

    print(f"[NEW USER] {username}")

    broadcast(
        f"{username} joined the virtual LAN.".encode()
    )

    client.send(
        "[CONNECTED TO VIRTUAL LAN SERVER]".encode()
    )

    thread = threading.Thread(
        target=handle_client,
        args=(client,)
    )

    thread.start()
