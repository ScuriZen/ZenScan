import nmap
from tqdm import tqdm
import time

def run_nmap_scan(target):
    print(f"\n[+] Running Nmap Scan on {target}...\n")
    
    scanner = nmap.PortScanner()
    
    # Perform scan and update progress bar dynamically
    scanner.scan(target, arguments="-sV")
    hosts = scanner.all_hosts()

    with tqdm(total=len(hosts), desc="Scanning Hosts", ncols=75, ascii=True, colour="blue") as pbar:
        for host in hosts:
            time.sleep(0.5)  # Simulating processing time
            pbar.update(1)  # Move progress bar forward
    
    print("\n[+] Nmap Scan Results:")
    for host in hosts:
        print(f"Host: {host} ({scanner[host].hostname()})")
        print("State:", scanner[host].state())
        for proto in scanner[host].all_protocols():
            print(f"Protocol: {proto}")
            ports = scanner[host][proto].keys()
            for port in ports:
                print(f"Port: {port}, State: {scanner[host][proto][port]['state']}")

    print("\n[+] Scan Completed!")
