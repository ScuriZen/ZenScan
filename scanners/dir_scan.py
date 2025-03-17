import requests
import os
import time
from tqdm import tqdm

# Common directories for Normal Scan
COMMON_DIRECTORIES = [
    "admin", "login", "dashboard", "backup", "config", "database", "api", "graphql",
    "server-status", "wp-admin", "wp-content", "wp-includes", ".git", ".env", "phpinfo.php"
]

def run_dir_scan(target):
    print(f"\n\033[94m[+] Directory Scanner for {target}\033[0m\n")
    print("[1] Normal Scan (Common directories)")
    print("[2] Advanced Scan (Custom Wordlist Brute Force)")

    scan_type = input("\nChoose scan mode (1 or 2): ").strip()

    if scan_type == "1":
        perform_scan(target, COMMON_DIRECTORIES, "Normal Scan")
    elif scan_type == "2":
        wordlist_path = input("\nEnter the path to your wordlist file: ").strip()
        if not os.path.exists(wordlist_path):
            print("\n❌ Wordlist file not found! Please provide a valid file path.")
            return
        with open(wordlist_path, "r", encoding="utf-8") as file:
            custom_dirs = [line.strip() for line in file.readlines()]
        perform_scan(target, custom_dirs, "Brute Force Scan")
    else:
        print("\n❌ Invalid choice! Please enter 1 or 2.")

def perform_scan(target, directories, scan_mode):
    print(f"\n\033[94m[+] Running {scan_mode} on {target}...\033[0m\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }

    pbar = tqdm(total=len(directories), desc=f"Scanning ({scan_mode})", ncols=75, ascii=True, colour="cyan")

    found_dirs = 0  # Counter for found directories

    for directory in directories:
        url = f"{target.rstrip('/')}/{directory}"
        try:
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                print(f"✅ Found | 200 | {url}")
                found_dirs += 1
            elif response.status_code in [301, 302]:
                print(f"🔀 Redirect | {response.status_code} | {url}")
                found_dirs += 1
            elif response.status_code == 403:
                print(f"⛔ Forbidden | {response.status_code} | {url}")
                found_dirs += 1

        except requests.exceptions.RequestException:
            pass  # Ignore timeouts or connection errors

        pbar.update(1)  # Move progress bar forward
        time.sleep(0.1)  # Slight delay to avoid detection

    pbar.close()

    # Final Summary
    print(f"\n\033[92m[✔] {scan_mode} Completed!\033[0m")
    if found_dirs == 0:
        print("\n❌ No directories found.")
    print("\n")
