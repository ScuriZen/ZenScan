import os

def run_nmap_scan(target):
    print(f"Running Nmap scan on {target}...")
    os.system(f"nmap -A {target}")

