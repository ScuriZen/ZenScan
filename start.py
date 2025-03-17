import os
import sys
import time
from banners import zen_banner
from scanners.nmap_scan import run_nmap_scan
from scanners.port_scan import run_port_scan
from scanners.sqlmap_scan import run_sqlmap_scan
from scanners.dir_scan import run_dir_scan
from scanners.wapiti_scan import run_wapiti_scan

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        zen_banner()
        print("\n[1] Nmap Scan")
        print("[2] Port Scan")
        print("[3] SQL Injection Scan")
        print("[4] Web Vulnerability Scan (Wapiti)")
        print("[5] Directory Scanner")
        print("[6] Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            target = input("\nEnter target domain/IP: ").strip()
            print("\n\033[93m[🔎] Starting Nmap Scan...\033[0m\n")
            run_nmap_scan(target)
        
        elif choice == "2":
            target = input("\nEnter target domain/IP: ").strip()
            print("\n\033[93m[🔎] Starting Port Scan...\033[0m\n")
            run_port_scan(target)
        
        elif choice == "3":
            target = input("\nEnter target URL: ").strip()
            print("\n\033[93m[🔎] Starting SQL Injection Scan...\033[0m\n")
            run_sqlmap_scan(target)
        
        elif choice == "4":
            target = input("\nEnter target URL: ").strip()
            print("\n\033[93m[🔎] Starting Web Vulnerability Scan...\033[0m\n")
            run_wapiti_scan(target)
        
        elif choice == "5":
            target = input("\nEnter target URL (e.g., https://example.com): ").strip()
            print("\n\033[93m[🔎] Starting Directory Scan...\033[0m\n")
            run_dir_scan(target)
        
        elif choice == "6":
            print("\n\033[91m[✘] Exiting ZenScan. Goodbye!\033[0m\n")
            sys.exit()
        
        else:
            print("\n\033[91m[✘] Invalid choice! Please try again.\033[0m")

        input("\n\033[94mPress Enter to continue...\033[0m\n")

if __name__ == "__main__":
    main()
