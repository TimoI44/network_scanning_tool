import sys
import os
from netaddr import IPNetwork
from scapy.all import sr1,IP,ICMP


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

    # Send ICMP packket to every host on the network
    # -> if the host respondes it is marked as online
    for host_ip in network.iter_hosts():
        scanned_hosts+=1
        print(f"Scanning: {scanned_hosts}/{total_hosts}", end="\r")

        if hostIsOnline(host_ip):
            live_hosts.append(str(host_ip))
            print(f"Host {host_ip} is online")

    return live_hosts



print(pingSweep("192.168.178.1", "24"))