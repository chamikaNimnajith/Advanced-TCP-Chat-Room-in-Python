import threading
import socket
import os

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

# Ensure bans.txt exists
if not os.path.exists("bans.txt"):
    open("bans.txt", "w").close()


def broadcast(message):
    for client in clients[:]:
        try:
            client.send(message)
        except:
            clients.remove(client)
            client.close()


def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break

            decoded_msg = msg.decode('ascii')
            user = nicknames[clients.index(client)]

            # KICK
            if decoded_msg.startswith('KICK'):
                if user == 'admin':
                    name_to_kick = decoded_msg[5:]
                    kick_user(name_to_kick)

            # BAN
            elif decoded_msg.startswith('BAN'):
                if user == 'admin':
                    name_to_ban = decoded_msg[4:]
                    kick_user(name_to_ban)
                    with open("bans.txt", 'a') as f:
                        f.write(name_to_ban + '\n')
                    print(f'{name_to_ban} was banned!')

            # NORMAL MESSAGE
            else:
                broadcast(msg)

        except:
            break

    # Remove disconnected client
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        client.close()
        broadcast(f'{nickname} left the chat'.encode('ascii'))


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        # Check ban list
        with open('bans.txt', 'r') as f:
            bans = f.read().splitlines()

        if nickname in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        # Admin authentication
        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def kick_user(name):
    if name in nicknames:
        index = nicknames.index(name)
        client_to_kick = clients[index]

        client_to_kick.send('You were kicked by an admin!'.encode('ascii'))
        client_to_kick.close()

        clients.remove(client_to_kick)
        nicknames.remove(name)

        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))


print("Server is Listening...")
receive()