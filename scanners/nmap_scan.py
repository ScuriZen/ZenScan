import os

def run_nmap_scan(target):
    print(f"\n\033[92m[+] Running Nmap scan on {target}...\033[0m\n")
    output = os.popen(f"nmap -A {target}").read()
    return output  # Return output to be displayed in start.py
