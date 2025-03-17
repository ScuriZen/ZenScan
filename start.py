import os
import sys
import time
from banners import zen_banner
from scanners.nmap_scan import run_nmap_scan
from scanners.port_scan import run_port_scan
from scanners.sqlmap_scan import run_sqlmap_scan
from scanners.dir_scan import run_dir_scan

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
            target = input("Enter target domain/IP: ").strip()
            run_nmap_scan(target)
        elif choice == "2":
            target = input("Enter target domain/IP: ").strip()
            run_port_scan(target)
        elif choice == "3":
            target = input("Enter target URL: ").strip()
            run_sqlmap_scan(target)
        elif choice == "4":
            target = input("Enter target URL: ").strip()
            run_wapiti_scan(target)
        elif choice == "5":
            target = input("Enter target URL (e.g., https://example.com): ").strip()
            run_dir_scan(target)
        elif choice == "6":
            print("Exiting ZenScan. Goodbye!")
            sys.exit()
        else:
            print("\n[✘] Invalid choice! Please try again.")

        input("\nPress Enter to continue...") 

if __name__ == "__main__":
    main()
