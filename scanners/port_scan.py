import socket
import time
from tqdm import tqdm

def run_port_scan(target):
    print("\n[+] Running Port Scan on:", target)

    # Simulating a loading progress bar
    for _ in tqdm(range(100), desc="Scanning", ncols=75, ascii=True, colour="cyan"):
        time.sleep(0.03)  # Simulating scan progress

    open_ports = []
    for port in range(20, 1025):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        s.close()

    print("\n[+] Open Ports Found:")
    if open_ports:
        for port in open_ports:
            print(f"Port {port} is Open")
    else:
        print("No open ports found.")

    print("\n[+] Scan Completed!")
