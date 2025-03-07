import socket
import time
from tqdm import tqdm

def run_port_scan(target):
    print(f"\n[+] Running Port Scan on {target}...\n")

    open_ports = []
    common_ports = list(range(20, 1025))  # List of ports to scan

    with tqdm(total=len(common_ports), desc="Scanning Ports", ncols=75, ascii=True, colour="cyan") as pbar:
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            s.close()
            pbar.update(1)  # Move progress bar forward

    print("\n[+] Open Ports Found:")
    if open_ports:
        for port in open_ports:
            print(f"✔ Port {port} is \033[92mOPEN\033[0m")
    else:
        print("❌ No open ports found.")

    print("\n[+] Scan Completed!")

