import os
import sys
import time
from banners import zen_banner
from scanners.nmap_scan import run_nmap_scan
from scanners.port_scan import run_port_scan
from scanners.sqlmap_scan import run_sqlmap_scan

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        zen_banner()
        print("\n[1] Nmap Scan")
        print("[2] Port Scan")
        print("[3] SQL Injection Scan")
        print("[4] Exit")

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
            print("Exiting ZenScan. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice! Please try again.")
        time.sleep(2)

if __name__ == "__main__":
    main()

