import socket
class server:
    
    def login(self, person_name):
        with socket.socket() as s:
            s.connect(('wgforge-srv.wargaming.net', 443))
            
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
            s.send(msg_serv)
            
            res = s.recv(4)
            size = int.from_bytes(s.recv(4), byteorder='little')
            d = s.recv(size)
    

    def logout(self):
        with socket.socket() as s:
            s.send(b'\x02\x00\x00\x00\x00\x00\x00\x00')




def map_get(self,layer_num):
    with socket.socket() as s:
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
            
            s.send(msg_serv)
            
            res = s.recv(4)
            size = int.from_bytes(s.recv(4), byteorder='little')
            d = s.recv(size)


def move(self, line_idx, speed, train_idx):
    with socket.socket() as s:
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
            
            s.send(msg_serv)
