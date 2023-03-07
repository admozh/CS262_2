import socket
import os
import threading
import time
import sys
import random
import json

EVENTS = {
    "MACHINE_ONE": 1,
    "MACHINE_TWO": 2,
    "BROADCAST": 3,
    "INTERNAL_EVENT": 4,
}

class Machine:
    def __init__(self,
                id: int = 0,
                host: str = "127.0.0.1",
                port: int = 8000,
                clock_rate: int = None,
                clock_range_size: int = 6,
                log_file: str = None,
                ) -> None:
        
        self.pid = id
        self.host = host
        self.port = port
        self.clock_rate = clock_rate
        self.clock_range_size = clock_range_size
        self.log_file = log_file
        self.logging = None
        self.logger_open: bool = False
        self.connections: list = []
        self.main_has_ended: bool = False
        self.receive_has_ended: bool = False
        self.set_clock()
        self.set_log_file()
        self.set_socket()

    def set_clock(self) -> None:
        if not self.clock_rate:
            self.clock_rate = 1 / random.randint(1, self.clock_range_size)

        else: self.clock_rate = 1 / self.clock_rate

        self.local_clock = 0

    def set_log_file(self) -> None:
        self.logger_open = True
        if not self.log_file:
            self.log_file = f"./logs/process_{self.pid}.log"
        else: self.log_file = "./logs/" + self.log_file

        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logging = open(self.log_file, 'a+')

    def receive_messages(self) -> None:

        while not self.receive_has_ended:
            try:
                conn, addr = self.receive_socket.accept()
                response = conn.recv(1024)
                self.queue.append(response)
            except:
                pass
    
    def set_socket(self) -> None:

        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_socket.bind((self.host, self.port))
        self.receive_socket.listen(5)

        self.queue: list = []
        self.main_receive_thread = threading.Thread(target=self.receive_messages)
        self.main_receive_thread.start()
    
    def connect_machines(self, connections: list = []) -> None:
        self.connections += connections

    def send_message(self, msg: str = "", receiver: int = None) -> None:
        
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_socket.connect(self.connections[receiver])

        self.send_socket.send(msg.encode())
        self.send_socket.close()

    def log_message(self, msg: str) -> None:

        current_time = time.time()

        # format the current time as a string
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))

        complete_message = f"{formatted_time}/{self.local_clock}/{msg}"
        
        self.logging.write(complete_message + '\n')
        

    def generate_event(self) -> None:
        
        msg = json.dumps({"sender" : f"process_{self.pid}",
                   "local_time" : self.local_clock,
                })

        EVENT_SIZE = 10
        event = random.randint(1, EVENT_SIZE)
        self_log = ""
        if event == EVENTS["MACHINE_ONE"]:
            self_log = f"Sent to machine_{event}"
            self.send_message(msg=msg, receiver=event - 1)

        elif event == EVENTS["MACHINE_TWO"]:
            self_log = f"Sent to machine_{event}"
            self.send_message(msg=msg, receiver=event - 1)

        elif event == EVENTS["BROADCAST"]:
            self_log = f"Broadcast to all machines"
            for i in range(len(self.connections)):
                self.send_message(msg=msg, receiver=i)

        else:
            self_log = "Internal event"
            time.sleep(.1)
        
        self.log_message(self_log)
        time.sleep(self.clock_rate)
            
            
    def main(self) -> None:

    
        while not self.main_has_ended:

            if self.queue:

                msg = json.loads(self.queue.pop(0))
                msg_time = msg['local_time']
                self.local_clock = max(self.local_clock, msg_time) + 1

                # Format receiving a message
                self.log_message(f"RecFrom:{msg['sender']}/QueueSize:{len(self.queue) + 1}")
                time.sleep(self.clock_rate)
                continue

            else:
                self.local_clock += 1
                self.generate_event()



    def shutdown(self) -> None:
        
        self.receive_socket.close()
        self.main_has_ended = True
        self.receive_has_ended = True
        self.main_receive_thread.join()

        if self.logger_open:
            self.logging.close()
        
        print(f"Shutdown vm_{self.pid}")

        


        
        


            



        


    
    
        
    
