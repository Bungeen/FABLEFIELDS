import socket
from _thread import *
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.1.44'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50,0", "1:100,100,0"]


def threaded_client(conn, pl_id):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        print(123)
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Received: " + reply)  # Info of Received

                arr = reply.split(":")  # Full decode data
                print(arr, 'arr')
                id = int(arr[0])  # id sender
                print(id, 'id')
                pos[id] = reply  # Save new data
                print(pos, 'pos')

                if id == 0: nid = 1  # Check who need to get new data
                if id == 1: nid = 0  # Check who need to get new data

                reply = pos[nid][:]  # COPY data
                print(reply, "reply")

                print("Sending: " + reply)  # Info of Sending

            conn.sendall(str.encode(reply))
        except:

            break

    pos[pl_id] = pos[pl_id][:-1] + '0'
    print(pos)
    print("Connection Closed")
    conn.close()


pl_id = 0

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, pl_id))
    pl_id += 1
