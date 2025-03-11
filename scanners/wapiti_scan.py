import os
import subprocess
from tqdm import tqdm

def run_wapiti_scan(target):
    print(f"\n[+] Running Wapiti Web Vulnerability Scan on {target}...\n")

    total_steps = 50  

    pbar = tqdm(total=total_steps, desc="Scanning", ncols=75, ascii=True, colour="yellow")

    try:
      ut
        command = f"wapiti -u {target} -f json -o results/"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in iter(process.stdout.readline, ""):
            if "attack" in line.lower() or "checking" in line.lower():
                pbar.update(1)  
            print(line.strip())  

        pbar.close()
        process.stdout.close()
    
    except Exception as e:
        print(f"\n[!] Error running Wapiti: {e}")

    print("\n[✔] Wapiti Scan Completed! Check the `results/` folder for detailed reports.\n")
