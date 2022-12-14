import socket
from _thread import *
import sys

import time


class Server:
    def __init__(self, registered_players):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.1.44'
        self.port = 5555

        self.server_ip = socket.gethostbyname(self.server)

        self.registered_players = registered_players

        try:
            self.s.bind((self.server, self.port))

        except socket.error as e:
            print(str(e))

        self.s.listen(2)
        print("Waiting for a connection")

        self.id_using_list = {}
        self.id_available_list = ['S0', 'S1', 'S1', 'S1']
        self.pos = ["0:50,50,0", "1:100,100,0"]

    def threaded_client(self, conn, player_id):
        # currentId = "2"  # NOT 1 OR 0. IT CAN'T BE ENCODED

        conn.send(str.encode(player_id))

        conn.settimeout(5)

        try:
            current_name_not_decoded = conn.recv(2048)
        except:
            print('Timeout')
            conn.close()
            return

        current_name = current_name_not_decoded.decode('utf-8')
        print(f'{current_name} was got')

        print('Save information about session...')
        print(self.id_available_list[0])
        self.id_using_list[current_name] = player_id
        print(player_id)
        conn.sendall(str.encode('GOOD'))
        while True:
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
                    id = int(arr[0][1:])  # id sender
                    print(id, 'id')
                    self.pos[id] = reply  # Save new data
                    print(self.pos, 'pos')

                    if id == 0: nid = 1  # Check who need to get new data
                    if id == 1: nid = 0  # Check who need to get new data

                    reply = self.pos[nid][:]  # COPY data
                    print(reply, "reply")

                    print("Sending: " + reply)  # Info of Sending

                conn.sendall(str.encode(reply))
            except:
                break

        # self.pos[player_id] = self.pos[player_id][:-1] + '0'
        print(self.pos)
        print("Connection Closed")
        self.id_available_list += [player_id]
        del self.id_using_list[current_name]
        print(self.id_available_list, self.id_using_list)

    def run(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to: ", addr)

            print('Checking...')
            if len(self.id_available_list) == 0:
                print('Not available space')
                self.s.close()
                continue

            print('Get id...')
            current_id = self.id_available_list[0]
            self.id_available_list.remove(current_id)
            print('Give thread...')
            start_new_thread(self.threaded_client, (conn, current_id))


tmp = Server(['user'])
tmp.run()
