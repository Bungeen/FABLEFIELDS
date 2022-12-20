import socket

import json
import ast


class Network:

    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ip

        # "192.168.1.44" # For this to work on your machine this must be equal to the ipv4
        # address of the machine running the server
        # You can find this address by typing ipconfig in CMD and copying the ipv4 address.
        # Again this must be the servers ipv4 address. This feild will be the same for all your clients.

        self.port = port  # 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()
        print(self.id)
        self.client.settimeout(3)

    def connect(self):
        self.client.settimeout(5)
        try:
            self.client.connect(self.addr)
            tmp = self.client.recv(2048).decode()
        except:
            return '0XE000'
        return tmp

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        packed_data = json.dumps(data)
        try:
            try:
                self.client.send(bytes(packed_data, encoding="utf-8"))
                # print('Continued', data)
            except:
                print('FAILED SENDING NETWORK', 'First')
                return '0XE000'
            try:
                reply = self.client.recv(2048).decode("utf-8")
                # print(reply)
                reply_data = json.loads(reply)
            except:
                print('FAILED GETTING NETWORK')
                return '0XE000'
            # print(reply_data)
            return reply_data
        except socket.error as e:
            return str(e)
