import requests
import dns.resolver
import concurrent.futures
import sys
import os
import json

# API sources for subdomain enumeration
API_SOURCES = [
    "https://crt.sh/?q=%.{domain}&output=json",
    "https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns",
    "https://api.threatminer.org/v2/domain.php?q={domain}&rt=5",
    "https://sonar.omnisint.io/subdomains/{domain}"
]

# Default wordlist for brute-force
DEFAULT_SUBDOMAIN_WORDLIST = [
    "admin", "mail", "ftp", "test", "dev", "staging", "api", "secure",
    "portal", "beta", "edge", "dashboard", "vpn", "office", "sso"
]

# Fetch subdomains from OSINT APIs
def fetch_subdomains_from_apis(domain):
    subdomains = set()
    for api in API_SOURCES:
        try:
            url = api.format(domain=domain)
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):  # Handling crt.sh response
                    for entry in data:
                        subdomains.add(entry['name_value'])
                elif 'passive_dns' in data:
                    for record in data['passive_dns']:
                        subdomains.add(record['hostname'])
                elif 'subdomains' in data:
                    subdomains.update(data['subdomains'])
        except:
            continue
    return subdomains

# Load custom wordlist from a file
def load_custom_wordlist(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    else:
        print("❌ File not found! Using default wordlist.")
        return DEFAULT_SUBDOMAIN_WORDLIST

# Check if a subdomain is active
def is_active(subdomain):
    try:
        dns.resolver.resolve(subdomain, 'A')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout):
        return False

# Brute-force subdomains using a wordlist
def brute_force_subdomains(domain, wordlist):
    subdomains = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_subdomain = {
            executor.submit(is_active, f"{sub}.{domain}"): f"{sub}.{domain}"
            for sub in wordlist
        }
        for future in concurrent.futures.as_completed(future_to_subdomain):
            subdomain = future_to_subdomain[future]
            if future.result():
                subdomains.add(subdomain)
    return subdomains

# Main function
def run_subdomain_scan():
    print("\n" + "="*50)
    print(" 🔎 ZenScan - Subdomain Enumeration")
    print("="*50)

    # Ask for scan method
    print("\n[1] OSINT API Enumeration")
    print("[2] Brute-force with Dictionary")
    choice = input("\nEnter your choice: ")

    if choice not in ["1", "2"]:
        print("❌ Invalid choice! Exiting.")
        return

    domain = input("\n🌍 Enter target domain: ")

    if choice == "1":
        print("\n🔍 Fetching subdomains from OSINT sources...")
        api_results = fetch_subdomains_from_apis(domain)
        print(f"✅ Found {len(api_results)} subdomains from APIs")

        for sub in sorted(api_results):
            print(f"🔹 {sub}")

    elif choice == "2":
        print("\n[1] Use Default Dictionary")
        print("[2] Provide Custom Dictionary Path")
        dict_choice = input("\nEnter your choice: ")

        if dict_choice == "2":
            file_path = input("📂 Enter dictionary file path: ")
            wordlist = load_custom_wordlist(file_path)
        else:
            wordlist = DEFAULT_SUBDOMAIN_WORDLIST

        print("\n🔍 Running brute-force subdomain enumeration...")
        brute_results = brute_force_subdomains(domain, wordlist)
        print(f"✅ Found {len(brute_results)} subdomains")

        for sub in sorted(brute_results):
            print(f"🔹 {sub}")

    print("\n🎯 Subdomain Enumeration Completed!")
    print("="*50)

# Execute if running as standalone script
if __name__ == "__main__":
    run_subdomain_scan()
