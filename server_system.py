import os
import socket
from _thread import *
import sys

import ast
import time
import json
import random

TEST_MAP = [['1 - 0', '1 - 0', '1 - 0', '1 - 0', '2 - 0', '2 - 0', '2 - 0', '2 - 0'],
            ['1 - 0', '3 - 0', '1 - 0', '2 - 0', '2 - 0', '1 - 0', '2 - 0', '1 - 0'],
            ['2 - 0', '1 - 0', '2 - 0', '2 - 0', '2 - 0', '1 - 0', '1 - 0', '1 - 0'],
            ['1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '2 - 0', '2 - 0'],
            ['2 - 0', '2 - 0', '2 - 0', '1 - 0', '2 - 0', '2 - 0', '2 - 0', '1 - 0'],
            ['2 - 0', '1 - 0', '1 - 0', '2 - 0', '2 - 0', '1 - 0', '2 - 0', '1 - 0']]

TEST_FLAG = True

DATA_BASE = {'8': [70, 20, 30]}

MONEY = 0


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
        self.logins_using_list = []
        # self.pos = ["0:50,50,0", "1:1114,1187,0"]
        self.pos = {
            'S0': {'Player Position': (0, 0), 'Player Status': 0, 'Player Animation Type': 0, 'Player Using State': 0,
                   'Package': {'World change': []}},
            'S1': {'Player Position': (0, 0), 'Player Status': 0, 'Player Animation Type': 0, 'Player Using State': 0,
                   'Package': {'World change': []}},
            'S2': {'Player Position': (0, 0), 'Player Status': 0, 'Player Animation Type': 0, 'Player Using State': 0,
                   'Package': {'World change': []}},
            'S3': {'Player Position': (0, 0), 'Player Status': 0, 'Player Animation Type': 0, 'Player Using State': 0,
                   'Package': {'World change': []}}}

    def server_game_cycle(self):
        while TEST_FLAG:
            time.sleep(0.2)
            changes = []
            for y in range(len(TEST_MAP)):
                for x in range(len(TEST_MAP[0])):
                    tile = TEST_MAP[y][x]
                    id_tile, id_state = map(str, tile.split(' - '))
                    if id_tile in DATA_BASE.keys():
                        if id_state in ['1', '2']:
                            # print(id_tile)
                            # os._exit(1)
                            choice = random.randint(1, DATA_BASE[id_tile][0])
                            if choice == 2:
                                if id_state == '1':
                                    id_state = '2'
                                elif id_state == '2':
                                    id_state = '3'
                            new_tile = f"{id_tile} - {id_state}"
                            changes += [(x, y), new_tile]
                            TEST_MAP[y][x] = f"{id_tile} - {id_state}"
                        elif id_state in ['4', '5']:
                            choice = random.randint(1, DATA_BASE[id_tile][1])
                            if choice == 2:
                                if id_state == '4':
                                    id_state = '5'
                                elif id_state == '5':
                                    id_state = '6'
                            choice = random.randint(1, DATA_BASE[id_tile][2])
                            if choice == 2:
                                if id_state == '4':
                                    id_state = '1'
                                elif id_state == '5':
                                    id_state = '2'
                            new_tile = f"{id_tile} - {id_state}"
                            changes += [(x, y), new_tile]
                            TEST_MAP[y][x] = f"{id_tile} - {id_state}"
            for key in self.pos.keys():
                if key in self.id_using_list:
                    self.pos[key]['Package']['World change'] += changes

    def threaded_client(self, conn, player_id):
        # currentId = "2"  # NOT 1 OR 0. IT CAN'T BE ENCODED

        conn.send(str.encode(player_id))

        conn.settimeout(5)

        try:
            current_name_not_decoded = conn.recv(4096)
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

        # Check login
        if current_name in self.logins_using_list:
            self.id_available_list += [player_id]
            self.id_available_list.sort()
            print("Somebody with same login are online")
            conn.close()
            return

        print('Save information about session...')
        print(self.id_available_list[0])
        self.id_using_list[player_id] = current_name
        self.logins_using_list += [current_name]
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
        # self.pos[player_id]['Status'] = 1
        # self.pos[int(player_id[1])] = f"{int(player_id[1])}:{self.registered_players[current_name]},0"
        print(self.pos)
        tmp_current_data = self.pos
        print(tmp_current_data)
        tmp_current_data[player_id]['Package']['Map'] = TEST_MAP
        # Give client information about self
        try:
            key = conn.recv(4096)
            key = key.decode('utf-8')
            print(key)
            packed_data = json.dumps(tmp_current_data[player_id])

            conn.sendall(bytes(packed_data, encoding="utf-8"))
        except:
            self.id_available_list += [player_id]
            self.id_available_list.sort()
            del self.id_using_list[player_id]
            self.logins_using_list.remove(current_name)
            print('Timeout')
            conn.close()
            return

        # ANIMATION_TYPES: 8-16 - Plants Types in hands
        while True:
            try:
                data = conn.recv(4096).decode('utf-8')
                print(type(data), "DATA")
                reply = ast.literal_eval(data)
                print(reply)
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    # self.pos[player_id]['Package'] = {}
                    print("Received: ", reply)  # Info of Received
                    sending_data = {}
                    print("Sending Data", sending_data)
                    cur_key = reply["ID"]
                    print(self.id_using_list, 'IS_USING')
                    for key in self.pos.keys():
                        print(key)
                        # if key == cur_key:
                        #    sending_data['Package'] = self.pos[key]['Package']
                        #    continue
                        sending_data[key] = self.pos[key]
                        if key in self.id_using_list:
                            self.pos[key]['Package']['World change'] += reply['Package']['World change']
                    print("Cur key", cur_key)
                    self.pos[cur_key] = {"Player Position": reply["Player Position"],
                                         "Player Status": reply["Player Status"],
                                         'Player Animation Type': reply['Player Animation Type'],
                                         'Player Using State': reply['Player Using State'],
                                         'Package': {'World change': []}}

                    # print(len(reply['Package']['World change']), reply['Package']['World change'])
                    for i in range(0, len(reply['Package']['World change']), 2):
                        try:
                            x, y = reply['Package']['World change'][i][0], \
                                   reply['Package']['World change'][i][1]
                            TEST_MAP[y][x] = reply['Package']['World change'][i + 1]
                        except:
                            continue
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

        # Reset animation and other states
        self.pos[player_id]['Player Using State'] = 0
        self.pos[player_id]['Player Animation Type'] = 0
        self.pos[player_id]['Package'] = {'World change': []}

        self.registered_players[current_name] = self.pos[player_id]
        self.pos[player_id]['Player Status'] = 0
        print(self.pos)
        self.id_available_list += [player_id]
        self.id_available_list.sort()
        del self.id_using_list[player_id]
        self.logins_using_list.remove(current_name)
        print(self.id_available_list, self.id_using_list, self.logins_using_list)

    def run(self):
        start_new_thread(self.server_game_cycle, ())
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


tmp = Server({'user': {'Player Position': (50, 50), 'Player Status': 1, 'Player Animation Type': 0,
                       'Player Using State': 0, 'Package': {'World change': []}},
              'tmp_1': {'Player Position': (150, 150), 'Player Status': 1, 'Player Animation Type': 0,
                        'Player Using State': 0, 'Package': {'World change': []}}})
tmp.run()
