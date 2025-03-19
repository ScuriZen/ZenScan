import socket
import time
from tqdm import tqdm

def run_port_scan(target):
    print("\n" + "="*50)
    print(f" 🔎 ZenScan - Running Port Scan on {target}")
    print("="*50)

    open_ports = []
    common_ports = list(range(20, 1025))  
    # common_ports = [21, 22, 23, 25, 53, 80, 443, 8080]

    with tqdm(total=len(common_ports), desc="Scanning Ports", ncols=75, ascii=True, colour="cyan") as pbar:
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            s.close()
            pbar.update(1) 

    print("\n[+] Open Ports Found:")
    if open_ports:
        for port in open_ports:
            print(f"✔ Port {port} is \033[92mOPEN\033[0m")
    else:
        print("❌ No open ports found.")

    print("\n[+] Scan Completed!")

