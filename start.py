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
            output = run_nmap_scan(target)
            print("\n\033[92m[✔] Nmap Scan Results:\033[0m")  # Green color output
            print(output)
        elif choice == "2":
            target = input("Enter target domain/IP: ").strip()
            output = run_port_scan(target)
            print("\n\033[94m[✔] Port Scan Results:\033[0m")  # Blue color output
            print(output)
        elif choice == "3":
            target = input("Enter target URL: ").strip()
            output = run_sqlmap_scan(target)
            print("\n\033[91m[✔] SQL Injection Scan Results:\033[0m")  # Red color output
            print(output)
        elif choice == "4":
            print("Exiting ZenScan. Goodbye!")
            sys.exit()
        else:
            print("\n\033[93m[✘] Invalid choice! Please try again.\033[0m")  # Yellow color output

        input("\nPress Enter to continue...")  # Pause before clearing the screen

if __name__ == "__main__":
    main()
