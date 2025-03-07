import nmap
from tqdm import tqdm
import time

def run_nmap_scan(target):
    print(f"\n[+] Running Advanced Nmap Scan on {target}...\n")
    
    scanner = nmap.PortScanner()
    
    # Perform scan and update progress bar dynamically
    scanner.scan(target, arguments="-sV -O -Pn")  # -sV: Service detection, -O: OS detection, -Pn: No ping scan

    hosts = scanner.all_hosts()

    with tqdm(total=len(hosts), desc="Scanning Hosts", ncols=75, ascii=True, colour="blue") as pbar:
        for host in hosts:
            time.sleep(0.5)  # Simulating processing time
            pbar.update(1)  # Move progress bar forward

    print("\n\033[92m[✔] Nmap Scan Results:\033[0m\n")

    for host in hosts:
        print(f"\n🌐 \033[1mHost:\033[0m {host} ({scanner[host].hostname()})")
        print(f"📡 \033[1mState:\033[0m {scanner[host].state()}")

        # Extract Operating System Information
        if "osmatch" in scanner[host]:
            print("\n🖥️ \033[1mOperating System Detected:\033[0m")
            for os in scanner[host]["osmatch"]:
                print(f"  - {os['name']} (Accuracy: {os['accuracy']}%)")

        # Extract MAC Address
        if "mac" in scanner[host]:
            print(f"\n🔗 \033[1mMAC Address:\033[0m {scanner[host]['mac']}")

        # Extract Port and Service Information
        for proto in scanner[host].all_protocols():
            print(f"\n🚀 \033[1mProtocol:\033[0m {proto.upper()}")

            ports = scanner[host][proto].keys()
            for port in ports:
                service = scanner[host][proto][port]
                print(f"  🔹 Port: {port} | State: {service['state']} | Service: {service.get('name', 'Unknown')}", end="")

                # Display version info if available
                if "product" in service and service["product"]:
                    print(f" | \033[93m{service['product']} {service.get('version', '')}\033[0m", end="")
                
                print("")  # New line

    print("\n\033[92m[✔] Scan Completed Successfully!\033[0m\n")
