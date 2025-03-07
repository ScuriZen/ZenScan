import socket

def run_port_scan(target):
    print(f"Scanning open ports on {target}...\n")
    common_ports = [21, 22, 23, 25, 53, 80, 443, 8080]
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()
