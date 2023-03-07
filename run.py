from process import *
import threading
import signal

NUM_MACHINES = 3

addresses = [("127.0.0.1", port) for port in range(8000, 8000 + NUM_MACHINES)]
machines = []
running_processes = []

def signal_handler(sig, frame):
    for machine in machines:
        machine.shutdown()
    for process in running_processes:
        process.join()
    sys.exit(0)

# Register the signal handler function to handle the SIGINT signal
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print(len(addresses))
    for id in range(len(addresses)):
        vm = Machine(id=id+1, host=addresses[id][0], port=addresses[id][1])
        vm.connect_machines(addresses[:id] + addresses[id+1:])
        machines.append(vm)

        with open(vm.log_file, 'a+') as file:
            file.write(f"{vm.pid}, {vm.clock_rate}" + '\n')
    
    for vm in machines:
        vm_process = threading.Thread(target=vm.main)
        running_processes.append(vm_process)
        vm_process.start()
        
