import os
from netaddr import IPNetwork
from scapy.all import sr1,IP,TCP
from concurrent.futures import ThreadPoolExecutor, as_completed
import config


# Settinig max threads to the cpu core count
max_threads = os.cpu_count()

# Scans the given port on the given ip using a SYN-Scan
# Note that the ACK package is not being sent -> we dont establish a full connection
# Firewalls may prevent the detection of open ports
def scan_port(ip, port):
    # Sending SYN request to the server at the given port
    response = sr1(IP(dst=ip)/TCP(dport=port, flags="S"), timeout=1, verbose=0)
    if response is not None and response[TCP].flags == "SA":
        return True
    return False

# Scans a list of top ports on the given ip and returns a list of open ports
def scan_top_ports(ip):
    open_ports = []
    total_ports = len(config.top_ports)

    # Using Threads to optimize performance
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
            
            # Scan every top port on our ip
            thread_output = {executor.submit(scan_port, ip, port): port for port in config.top_ports}
            
            # Getting results
            for i, future in enumerate(as_completed(thread_output)):
                port = thread_output[future]
                res = future.result()

                print(f"Scanning: {i}/{total_ports} ports on {ip}", end="\r")
                if res == True:
                    open_ports.append(port)
                    print(f"\r\033[KPort {port} is open ({ip})")

    return open_ports

