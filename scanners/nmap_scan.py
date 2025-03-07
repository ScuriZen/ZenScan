import nmap
from tqdm import tqdm
import time

def run_nmap_scan(target):
    print(f"\n[+] Running Advanced Nmap Scan on {target}...\n")
    
    scanner = nmap.PortScanner()

    scanner.scan(target, arguments="-sV -O -Pn")  

    hosts = scanner.all_hosts()

    with tqdm(total=len(hosts), desc="Scanning Hosts", ncols=75, ascii=True, colour="blue") as pbar:
        for host in hosts:
            time.sleep(0.5)  
            pbar.update(1)  

    print("\n\033[92m[✔] Nmap Scan Results:\033[0m\n")

    for host in hosts:
        print(f"\n🌐 \033[1mHost:\033[0m {host} ({scanner[host].hostname()})")
        print(f"📡 \033[1mState:\033[0m {scanner[host].state()}")


        if "osmatch" in scanner[host]:
            print("\n🖥️ \033[1mOperating System Detected:\033[0m")
            for os in scanner[host]["osmatch"]:
                print(f"  - {os['name']} (Accuracy: {os['accuracy']}%)")

   
        if "mac" in scanner[host]:
            print(f"\n🔗 \033[1mMAC Address:\033[0m {scanner[host]['mac']}")


        for proto in scanner[host].all_protocols():
            print(f"\n🚀 \033[1mProtocol:\033[0m {proto.upper()}")

            ports = scanner[host][proto].keys()
            for port in ports:
                service = scanner[host][proto][port]
                print(f"  🔹 Port: {port} | State: {service['state']} | Service: {service.get('name', 'Unknown')}", end="")

                if "product" in service and service["product"]:
                    print(f" | \033[93m{service['product']} {service.get('version', '')}\033[0m", end="")
                
                print("")  

    print("\n\033[92m[✔] Scan Completed Successfully!\033[0m\n")
