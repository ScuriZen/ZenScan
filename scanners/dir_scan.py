import requests
import os
import time
from tqdm import tqdm

# Common directories to check
COMMON_DIRECTORIES = [
    "admin", "login", "dashboard", "backup", "config", "database", "api", "graphql",
    "server-status", "wp-admin", "wp-content", "wp-includes", ".git", ".env", "phpinfo.php"
]

def run_dir_scan(target):
    print(f"\n\033[94m[+] Running Advanced Directory Scan on {target}...\033[0m\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    pbar = tqdm(total=len(COMMON_DIRECTORIES), desc="Scanning Directories", ncols=75, ascii=True, colour="cyan")

    found_dirs = []
    
    for directory in COMMON_DIRECTORIES:
        url = f"{target.rstrip('/')}/{directory}"
        try:
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                found_dirs.append((url, response.status_code, "✅ Found"))
            elif response.status_code in [301, 302]:
                found_dirs.append((url, response.status_code, "🔀 Redirect"))
            elif response.status_code in [403]:
                found_dirs.append((url, response.status_code, "⛔ Forbidden"))

        except requests.exceptions.RequestException:
            pass 

        pbar.update(1) 
        time.sleep(0.1)  

    pbar.close()

    print("\n\033[92m[✔] Directory Scan Results:\033[0m\n")
    if found_dirs:
        for url, status, message in found_dirs:
            print(f"{message} | {status} | {url}")
    else:
        print("\n❌ No directories found.")

    print("\n\033[92m[✔] Scan Completed Successfully!\033[0m\n")
