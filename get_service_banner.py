import socket


# Attempts to get the service banner by sending an Http Get request to the server
# -> The server should respond with a banner containing informations such as software and version
# Note: Not all servers reply to this
def get_service_banner(ip, port):
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(3)
        connection.connect((ip, port))
        # Sending an Http request to the server
        connection.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        banner = connection.recv(1024)
        connection.close()

        # Returning the banner
        return banner.decode('utf-8', errors='ignore')
    except Exception:
        return None