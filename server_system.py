import os
import socket
from _thread import *
import sys

import ast
import time
import json
import random

TEST_MAP = [['1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0'],
            ['1 - 0', '3 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0'],
            ['1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0'],
            ['1 - 0', '1 - 0', '1 - 0', '1 - 0', '6 - 0', '1 - 0', '1 - 0', '1 - 0'],
            ['1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '5 - 0', '1 - 0'],
            ['1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0', '1 - 0']]


# TEST_FLAG = True

# DATA_BASE = {'8': [70, 20, 30]}

# MONEY = 0

# AVAILABLE_ITEMS = ['8']


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

        self.available_items = ['8']
        self.costs_for_buy = {'8': 0, '9': 10, '10': 25, '11': 25, '12': 25, '13': 25, '14': 25, '15': 25, '16': 25,
                              '17': 25}
        self.costs_for_sell = {'8': 3, '9': 6, '10': 7, '11': 7, '12': 7, '13': 7, '14': 7, '15': 7, '16': 7, '17': 7}
        self.money = 0
        self.data_base = {'8': [70, 20, 30], '9': [100, 20, 10], '10': [100, 20, 10], '11': [100, 20, 10],
                          '12': [100, 20, 10], '13': [100, 20, 10], '14': [100, 20, 10], '15': [100, 20, 10],
                          '16': [100, 20, 10], '17': [100, 20, 10]}
        self.game_going = 0
        self.timer = 1000

    def server_game_cycle(self):
        while self.game_going:
            time.sleep(0.2)
            self.timer -= 0.2
            changes = []
            for y in range(len(TEST_MAP)):
                for x in range(len(TEST_MAP[0])):
                    tile = TEST_MAP[y][x]
                    id_tile, id_state = map(str, tile.split(' - '))
                    if id_tile in self.data_base.keys():
                        if id_state in ['1', '2']:
                            # print(id_tile)
                            # os._exit(1)
                            choice = random.randint(1, self.data_base[id_tile][0])
                            if choice == 2:
                                if id_state == '1':
                                    id_state = '2'
                                elif id_state == '2':
                                    id_state = '3'
                            new_tile = f"{id_tile} - {id_state}"
                            changes += [(x, y), new_tile]
                            TEST_MAP[y][x] = f"{id_tile} - {id_state}"
                        elif id_state in ['4', '5']:
                            choice = random.randint(1, self.data_base[id_tile][1])
                            if choice == 2:
                                if id_state == '4':
                                    id_state = '5'
                                elif id_state == '5':
                                    id_state = '6'
                            choice = random.randint(1, self.data_base[id_tile][2])
                            if choice == 2:
                                if id_state == '4':
                                    id_state = '1'
                                elif id_state == '5':
                                    id_state = '2'
                        if id_state in ['6']:
                            choice = random.randint(1, self.data_base[id_tile][2])
                            if choice == 2:
                                id_state = '3'
                    if id_tile == '0':
                        if id_state == '1':
                            choice = random.randint(1, 30)
                            if choice == 2:
                                id_state = '0'
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
            current_name_not_decoded = conn.recv(65536)
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

        print(self.pos)
        tmp_current_data = self.pos
        print(tmp_current_data)
        tmp_current_data[player_id]['Package']['Map'] = TEST_MAP
        tmp_current_data[player_id]['Package']['Available Items'] = {'Seeds': self.available_items}
        tmp_current_data[player_id]['Package']['Money'] = self.money
        tmp_current_data[player_id]['Package']['Costs'] = self.costs_for_buy
        tmp_current_data[player_id]['Package']['Time'] = self.timer
        tmp_current_data[player_id]['Package']['Game Status'] = self.game_going

        # Give client information about self
        try:
            key = conn.recv(65536)
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

        # ANIMATION_TYPES: 8-16 - Plants Types in hands, 38-46 - SELL, 19-26 - BUY TYPE
        while True:
            print("Start cycle")
            try:
                data = conn.recv(65536).decode('utf-8')
                print(type(data), "DATA")
                reply = ast.literal_eval(data)
                print(reply)
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:

                    # self.pos[player_id]['Package'] = {}
                    print("Received: ", reply)  # Info of Received

                    # Logistic interactions
                    if reply["Player Animation Type"] in range(19, 27):
                        if int(reply['Player Animation Type']) - 10 not in self.available_items and \
                                self.costs_for_buy[str(int(reply['Player Animation Type']) - 10)] <= self.money:
                            self.available_items += [str(int(reply['Player Animation Type']) - 10)]
                            self.money -= self.costs_for_buy[str(int(reply['Player Animation Type']) - 10)]
                        reply["Player Animation Type"] = 0
                    elif reply["Player Animation Type"] in range(38, 47):
                        print("ID SELL", str(int(reply['Player Animation Type'] - 30)))
                        self.money += self.costs_for_sell[str(int(reply['Player Animation Type'] - 30))]
                        reply["Player Animation Type"] = 0

                    sending_data = {}
                    print("Sending Data", sending_data)
                    cur_key = reply["ID"]
                    print(self.id_using_list, 'IS_USING')
                    for key in self.pos.keys():
                        print(key)
                        sending_data[key] = self.pos[key]
                        if key in self.id_using_list:
                            self.pos[key]['Package']['World change'] += reply['Package']['World change']
                            print(self.pos[key]['Package'], self.money)
                            self.pos[key]['Package']['Money'] = self.money
                            self.pos[key]['Package']['Available Items'] = {'Seeds': self.available_items}
                            self.pos[key]['Package']['Time'] = self.timer
                            self.pos[key]['Package']['Game Status'] = self.game_going
                    print("Cur key", cur_key)

                    self.pos[cur_key] = {"Player Position": reply["Player Position"],
                                         "Player Status": reply["Player Status"],
                                         'Player Animation Type': reply['Player Animation Type'],
                                         'Player Using State': reply['Player Using State'],
                                         'Package': {'World change': [], 'Money': self.money,
                                                     'Available Items': {'Seeds': self.available_items}}}

                    print("Saved data", self.pos[cur_key])

                    # print(len(reply['Package']['World change']), reply['Package']['World change'])
                    for i in range(0, len(reply['Package']['World change']), 2):
                        try:
                            x, y = reply['Package']['World change'][i][0], \
                                   reply['Package']['World change'][i][1]
                            TEST_MAP[y][x] = reply['Package']['World change'][i + 1]
                        except:
                            continue

                    for x in self.id_using_list:
                        if self.pos[x]['Player Animation Type'] == 2:
                            continue
                        else:
                            break
                    else:
                        if not self.game_going and len(self.id_using_list) > 0:
                            self.game_going = 1
                            start_new_thread(self.server_game_cycle, ())
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
                       'Player Using State': 0,
                       'Package': {'World change': []}},
              'tmp_1': {'Player Position': (150, 150), 'Player Status': 1, 'Player Animation Type': 0,
                        'Player Using State': 0,
                        'Package': {'World change': []}}})
tmp.run()
