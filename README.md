=========================================================
PYTHON SOCKET CHAT APPLICATION
=========================================================

Description:
------------
This is a simple multi-client chat application built using
Python socket programming and threading.

It supports:
- Multiple clients
- Nickname system
- Admin login with password
- Kick users (admin only)
- Ban users (admin only)
- Persistent ban list using bans.txt


=========================================================
PROJECT FILES
=========================================================

server.py  -> Main chat server
client.py  -> Chat client program
bans.txt   -> Stores banned usernames (auto-created)


=========================================================
REQUIREMENTS
=========================================================

- Python 3.x
- No external libraries needed
- Works on Windows / Linux / macOS


=========================================================
HOW TO RUN
=========================================================

STEP 1: Start the Server

Open terminal in project folder and run:

    python(srver.py)

You should see:

    Server is Listening...

Server runs on:
    Host: 127.0.0.1
    Port: 55555


STEP 2: Start Clients

Open a new terminal for each user and run:

    python client.py

Enter a nickname when prompted.


=========================================================
ADMIN LOGIN
=========================================================

To login as admin:

Nickname: admin
Password: adminpass

If password is incorrect:
Connection will be refused.


=========================================================
USAGE
=========================================================

Normal Chat:
------------
Just type message and press Enter.

Example:
    Hello everyone


Admin Commands:
---------------

Kick a user:
    /kick username

Example:
    /kick john

Ban a user:
    /ban username

Example:
    /ban john

When a user is banned:
- They are kicked immediately
- Their username is saved in bans.txt
- They cannot reconnect


=========================================================
HOW IT WORKS
=========================================================

Server:
-------
- Accepts multiple client connections
- Stores clients and nicknames in lists
- Creates a new thread per client
- Broadcasts messages to all users
- Handles admin commands (KICK / BAN)
- Reads and writes banned users to bans.txt

Client:
-------
- Connects to server
- Sends nickname
- Handles admin authentication
- Runs 2 threads:
    1) receive() -> listens for messages
    2) write()   -> sends messages
- Parses admin commands locally


=========================================================
NOTES
=========================================================

- This application runs on localhost only (127.0.0.1)
- To allow external connections, change server host to:

    host = '0.0.0.0'

- Make sure port 55555 is not already in use.
- bans.txt must exist (server auto-creates if missing).



