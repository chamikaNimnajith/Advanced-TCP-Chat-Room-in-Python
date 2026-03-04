import socket
import threading

nickname = input("Choose a nickname: ")

password = None
if nickname == 'admin':
    password = input("Enter password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_thread = False


def receive():
    global stop_thread

    while not stop_thread:
        try:
            message = client.recv(1024)

            if not message:
                print("Disconnected from server.")
                break

            message = message.decode('ascii')

            if message == 'NICK':
                client.send(nickname.encode('ascii'))

            elif message == 'PASS':
                client.send(password.encode('ascii'))

            elif message == 'REFUSE':
                print("Connection refused! Wrong admin password.")
                stop_thread = True

            elif message == 'BAN':
                print("Connection refused! You are banned.")
                stop_thread = True

            else:
                print(message)

        except:
            print("Connection closed.")
            break

    client.close()
    stop_thread = True


def write():
    global stop_thread

    while not stop_thread:
        try:
            user_input = input()

            # Admin commands
            if user_input.startswith('/'):
                if nickname != 'admin':
                    print("Only admin can use commands!")
                    continue

                if user_input.startswith('/kick '):
                    target = user_input[6:]
                    client.send(f'KICK {target}'.encode('ascii'))

                elif user_input.startswith('/ban '):
                    target = user_input[5:]
                    client.send(f'BAN {target}'.encode('ascii'))

                else:
                    print("Unknown command.")

            else:
                message = f'{nickname} : {user_input}'
                client.send(message.encode('ascii'))

        except:
            break

    stop_thread = True
    client.close()


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()