import socket
import threading
import os

# =========================
# CONFIG
# =========================

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 5555))

# =========================
# SOCKET SETUP
# =========================

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

print(f"[SERVER STARTED] Port: {PORT}")

# =========================
# STORAGE
# =========================

clients = []
usernames = {}

# =========================
# BROADCAST
# =========================

def broadcast(message, sender=None):

    for client in clients:

        if client != sender:

            try:

                client.sendall(message)

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
            f"{username} left the server.".encode()
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

            decoded = message.decode().strip()

            print(decoded)

            broadcast(
                decoded.encode(),
                client
            )

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
    client.sendall(b"USERNAME\n")

    username = client.recv(1024).decode().strip()

    usernames[client] = username

    clients.append(client)

    print(f"[NEW USER] {username}")

    broadcast(
        f"{username} joined the server.".encode()
    )

    client.sendall(
        b"[CONNECTED TO SERVER]"
    )

    thread = threading.Thread(
        target=handle_client,
        args=(client,)
    )

    thread.start()
