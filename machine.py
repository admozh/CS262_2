import threading
import random
from _thread import *
import sys
import time
import socket

# things to have
# run / random
# send
# receive
# log

# todo
# listen
# shutdown

HOST = "127.0.0.1"
LOG = []
PORTS = [8000, 8001, 8002]


class Machine(threading.Thread):

    # initialize each machine
    def __init__(self, id, clock_rate):
        threading.Thread.__init__(self)
        # set up network queue, log file, logical closk and clock rate
        self.id = id
        self.networks_queue = []
        self.sockets = {}
        self.logical_clock = 0
        self.log_file = open(f"vm_{id}.log", "w")
        self.connections = {}
        self.id_address = {0, 1, 2}

    def listen(s):
        while True:
            data = s.recv(1024)
            if not data:
                return
            print('Received message: ' + data.decode())

    def create_socket(self):
        # creates socket object for machine
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORTS[self.id]))
        # server can accept connections
        s.listen()
        print(f'{self.id} listening on {HOST}:{PORTS[self.id]}')

        for ip in self.id_address and ip != self.id:
            conn, addr = s.accept()
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            start_new_thread(listen, (conn,))
            self.sockets[ip] = conn

    # connects to other machines

    def connect(self):
        for ip in self.id_address:
            if ip != self.id:
                try:
                    self.sockets[ip].connect((HOST, PORTS[ip]))
                    print(
                        f'Machine {self.id} and {ip} are successfully connected')
                    break
                except:
                    continue

    def update_logical_clock(self, time):
        self.logical_clock = max(self.logical_clock, time) + 1

    def log(self, event):
        timestamp = time.time()
        self.log_file.write(
            f"{event} at {timestamp}, logical clock={self.logical_clock}\n")

    def receive(self, message):
        self.update_logical_clock(message["time"])
        self.network_queue.append(message)
        self.log_event(
            f"Received message {message} from {message['from']}, network queue size={len(self.network_queue)}")

    def send(self, message):
        for socket in self.sockets:
            socket.send(message)
        self.update_logical_clock(self.logical_clock)
        self.log_event(
            f"Sent message {message} to {len(self.sockets)} machine(s)")

    def run(self):
        self.create_socket()
        self.connect()

        while True:
            time.sleep(1 / self.clock_rate)
            if len(self.network_queue) > 0:
                message = self.network_queue.pop(0)
                self.update_logical_clock(message["time"])
                self.log_event(
                    f"Processed message {message}, network queue size={len(self.network_queue)}")
            else:
                event = random.randint(1, 10)
                if event == 1:
                    message = {"from": self.id, "time": self.logical_clock}
                    self.send(str(message))
                elif event == 2:
                    message = {"from": self.id, "time": self.logical_clock}
                    self.send(str(message))
                elif event == 3:
                    message = {"from": self.id, "time": self.logical_clock}
                    self.send(str(message))
                else:
                    self.update_logical_clock(self.logical_clock)
                    self.log_event(
                        f"Internal event, logical clock={self.logical_clock}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('please enter machine id and number between 1-6')
    tick = int(sys.argv[2])
    id = int(sys.argv[1])
    if not id in {0, 1, 2}:
        print('invalid machine id number')
    m = Machine(id, tick)
    m.run()
