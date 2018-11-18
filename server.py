import socket


class ServerConnection:
    def __init__(self):
        self.__socket = socket.socket()
        self.__socket.connect(('wgforge-srv.wargaming.net', 443))

    def login(self, person_name):
        action = 1
        action_byte = (action).to_bytes(4, byteorder='little')
            
        msg_fp = "{\"name\":\""
        person_name = "Boris"
        msg_lp = "\"}"

        msg = msg_fp + person_name + msg_lp
        msg_len = len(str(msg))
            
        msg_len_byte = (msg_len).to_bytes(4, byteorder='little')
            
        msg_byte = msg.encode()
        msg_serv = action_byte + msg_len_byte + msg_byte
        self.__socket.send(msg_serv)
            
        res = self.__socket.recv(4)
        size = int.from_bytes(self.__socket.recv(4), byteorder='little')
        d = self.__socket.recv(size)

    def logout(self):
        self.__socket.send(b'\x02\x00\x00\x00\x00\x00\x00\x00')

    def map_get(self, layer_num):
        action = 10
        action_byte = (action).to_bytes(4, byteorder='little')
            
        msg_fp = "{\"layer\":"
        layer_num = '0'
        msg_lp = "}"
            
        msg = msg_fp + layer_num + msg_lp
        msg_len = len(str(msg))
            
        msg_len_byte = (msg_len).to_bytes(4, byteorder='little')
            
        msg_byte = msg.encode()
        msg_serv = action_byte + msg_len_byte + msg_byte
            
        self.__socket.send(msg_serv)
            
        res = self.__socket.recv(4)
        size = int.from_bytes(self.__socket.recv(4), byteorder='little')
        d = self.__socket.recv(size)

    def move(self, line_idx, speed, train_idx):
        action = 3
        action_byte = (action).to_bytes(4, byteorder='little')
            
        msg_fp = "{\"line_idx\":"
        line_idx = '193'
        msg_mp = ",\"speed\":"
        speed = '1'
        msg_mmp = ",\"train_idx\":"
        train_idx = '1'
        msg_lp = "}"
            
        msg = msg_fp + line_idx + msg_mp + speed + msg_mmp + train_idx + msg_lp
        msg_len = len(str(msg))
            
        msg_len_byte = (msg_len).to_bytes(4, byteorder='little')
            
        msg_byte = msg.encode()
        msg_serv = action_byte + msg_len_byte + msg_byte
            
        self.__socket.send(msg_serv)
