import os
import subprocess
from tqdm import tqdm

def run_sqlmap_scan(target):
    print(f"\n[+] Running SQL Injection Scan on {target}...\n")

    command = f"sqlmap -u {target} --dbs --crawl 2 --batch"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    total_lines = 50  
    pbar = tqdm(total=total_lines, desc="Scanning SQLi", ncols=75, ascii=True, colour="red")

    for line in iter(process.stdout.readline, ""):
        if "testing connection" in line.lower() or "checking" in line.lower():
            pbar.update(1)  
        print(line.strip()) 

    pbar.close()
    process.stdout.close()
    print("\n[+] SQL Injection Scan Completed!")
