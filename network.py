import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.162.165"
        self.port = 5010
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            print(f"Connected to server at {self.addr}")
            player_id= self.client.recv(2048).decode()
            print(f"Received player ID: {player_id}")
            return player_id
        except Exception as e:
            print(f"Connection error: {e}")
            return None  # Explicitly return None if connection fails

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)

