# Author: Timo Ihbe
import sys
import logging
import os
from netaddr import IPNetwork
from scapy.all import sr1,IP,ICMP,Ether
from concurrent.futures import ThreadPoolExecutor, as_completed

# Settinig max threads to the cpu core count
max_threads = os.cpu_count()
# Surpressing scapy warnings, because console would be full of: WARNING: MAC address to reach destination not found. Using broadcast.
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Send ICMP packket to the host
# -> returns True if the host respondes
def hostIsOnline(hostIp):
    # Here the actual packet is made, send and an answer recieved using scapy
    res = sr1(IP(dst=str(hostIp))/ICMP(), timeout=1, verbose=0)
    if res is not None:
        return True
    return False

# Enter network and netmask accordingly -> 192.145.184.1/24: network="192.145.184.1"; netmask="24"
# returns an array of strings with live host ip's
def pingSweep(network, netmask):

    live_hosts = []
    total_hosts = 0
    scanned_hosts = 0
    network = IPNetwork(network + "/" + netmask)

    # Get total number of possible hosts
    for host_ip in network.iter_hosts():
        total_hosts+=1

    # Using Threads to optimize performance
    with ThreadPoolExecutor(max_workers=max_threads) as executor:

        # Send ICMP packket to every host on the network
        # -> if the host respondes it is marked as online
        thread_output = {executor.submit(hostIsOnline, host): host for host in network.iter_hosts()}

        for future in as_completed(thread_output):

            host = thread_output[future]
            res = future.result()

            scanned_hosts+=1
            print(f"Scanning: {scanned_hosts}/{total_hosts}", end="\r")

            if res == True:
                live_hosts.append(str(host))
                print(f"Host {host} is online")

    return live_hosts



print(pingSweep("192.168.178.1", "24"))