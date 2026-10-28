from ping_sweep import ping_sweep
from scan_ports import scan_port, scan_top_ports

#print(ping_sweep("192.168.178.1", "24"))

# Scans every possible ip to check if the host is up
# -> on every online host scan top ports
def full_network_scan(ip, netmask):
    ip_to_ports = {}
    live_hosts = ping_sweep(ip, netmask)

    for host_ip in live_hosts:
        ip_to_ports[host_ip] = scan_top_ports(host_ip)

    print("\r\033[K#### RESULTS: ####")

    for host, ports in ip_to_ports.items():
        print(f"--- IP: {host} ---")
        if ports is not None:
            for port in ports:
                print(f" {port} | open")
        else:
            print(" No open ports discoverd")

full_network_scan("192.168.178.0", "24")