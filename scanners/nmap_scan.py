import time
import nmap
from tqdm import tqdm

def run_nmap_scan(target):
    print("\n[+] Running Nmap Scan on:", target)
    
    # Simulating a loading progress bar
    for _ in tqdm(range(100), desc="Scanning", ncols=75, ascii=True, colour="blue"):
        time.sleep(0.03)  # Simulating scan progress
    
    scanner = nmap.PortScanner()
    scanner.scan(target, arguments="-sV")

    print("\n[+] Nmap Scan Results:")
    for host in scanner.all_hosts():
        print(f"Host: {host} ({scanner[host].hostname()})")
        print("State:", scanner[host].state())
        for proto in scanner[host].all_protocols():
            print(f"Protocol: {proto}")
            ports = scanner[host][proto].keys()
            for port in ports:
                print(f"Port: {port}, State: {scanner[host][proto][port]['state']}")

    print("\n[+] Scan Completed!")
