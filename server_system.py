import socket
from _thread import *
import sys

import ast
import time
import json


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
        self.id_available_list = ['S0', 'S1', 'S2', 'S3']
        # self.pos = ["0:50,50,0", "1:1114,1187,0"]
        self.pos = {'S0': {'Player Position': (50, 50), 'Player Active': 0},
                    'S1': {'Player Position': (1114, 1187), 'Player Active': 0}}

    def threaded_client(self, conn, player_id):
        # currentId = "2"  # NOT 1 OR 0. IT CAN'T BE ENCODED

        conn.send(str.encode(player_id))

        conn.settimeout(5)

        try:
            current_name_not_decoded = conn.recv(2048)
        except:
            self.id_available_list += [player_id]
            self.id_available_list.sort()
            print('Timeout')
            conn.close()
            return

        current_name_tmp = current_name_not_decoded.decode('utf-8')
        print(current_name_tmp)
        current_name = json.loads(current_name_tmp)  # json.load(current_name_tmp)
        print(f'{current_name} was got')

        print('Save information about session...')
        print(self.id_available_list[0])
        self.id_using_list[player_id] = current_name
        print(player_id)
        conn.send(bytes(json.dumps("GOOD"), encoding="utf-8"))
        print('SENDED')
        print(current_name, self.registered_players, self.registered_players.keys())

        # Checking for information about player
        if current_name in self.registered_players.keys():
            for key in self.registered_players[current_name].keys():
                try:
                    self.pos[player_id][key] = self.registered_players[current_name][key]
                except:
                    print(player_id, key, current_name)
                    sys.exit()
            # self.pos[int(player_id[1])] = f"{int(player_id[1])}:{self.registered_players[current_name]},0"
        print(self.pos)

        # Give client information about self
        try:
            key = conn.recv(2048)
            key = key.decode('utf-8')
            print(key)
            packed_data = json.dumps(self.pos[player_id])

            conn.sendall(bytes(packed_data, encoding="utf-8"))
        except:
            self.id_available_list += [player_id]
            self.id_available_list.sort()
            del self.id_using_list[player_id]
            print('Timeout')
            conn.close()
            return

        while True:
            try:
                data = conn.recv(2048).decode('utf-8')
                print(type(data), "DATA")
                reply = ast.literal_eval(data)
                print(reply)
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    print("Received: ", reply)  # Info of Received
                    sending_data = {}
                    print("Sending Data", sending_data)
                    cur_key = reply["ID"]
                    print(self.id_using_list, 'IS_USING')
                    for key in self.id_using_list.keys():
                        print(key)
                        if key == cur_key:
                            continue
                        sending_data[key] = self.pos[key]
                    print("Cur key", cur_key)
                    self.pos[cur_key] = {"Player Position": reply["Player Position"],
                                         "Player Active": reply["Player Active"]}
                    # arr = reply.split(":")  # Full decode data
                    # print(arr, 'arr')
                    # id = int(arr[0][1:])  # id sender
                    # print(id, 'id')
                    # self.pos[id] = reply  # Save new data
                    # print(self.pos, 'pos')
                #
                # if id == 0: nid = 1  # Check who need to get new data
                # if id == 1: nid = 0  # Check who need to get new data
                #
                # reply = self.pos[nid][:]  # COPY data
                # print(reply, "reply")
                #
                # print("Sending: " + reply)  # Info of Sending
                sending_data_packed = json.dumps(sending_data)
                conn.sendall(bytes(sending_data_packed, encoding="utf-8"))
            except:
                break

        # self.pos[player_id] = self.pos[player_id][:-1] + '0'
        print(self.pos)
        print("Connection Closed")
        self.id_available_list += [player_id]
        self.id_available_list.sort()
        del self.id_using_list[player_id]
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


tmp = Server({'user': {'Player Position': (1214, 1287)}, 'tmp_1': {'Player Position': (800, 700)}})
tmp.run()
