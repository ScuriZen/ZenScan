import requests
import dns.resolver
import concurrent.futures
import json
import sys
import os

# OSINT API Sources
API_SOURCES = [
    "https://crt.sh/?q=%.{domain}&output=json",
    "https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns",
    "https://api.threatminer.org/v2/domain.php?q={domain}&rt=5",
    "https://sonar.omnisint.io/subdomains/{domain}"
]

# Default wordlist for brute-force
DEFAULT_WORDLIST = [
    "admin", "mail", "webmail", "ftp", "test", "dev", "staging", "api", "secure",
    "vpn", "portal", "blog", "beta", "dashboard", "sso", "app", "auth", "download"
]

# Check if subdomain is active (Handles Errors)
def is_active(subdomain):
    if not subdomain or subdomain.startswith("."):  # Avoid empty labels
        return False

    try:
        dns.resolver.resolve(subdomain, 'A')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout, dns.name.EmptyLabel):
        return False

# OSINT API Enumeration
def fetch_subdomains_from_apis(domain):
    subdomains = set()
    print("\n🔍 Fetching subdomains from OSINT sources...")
    for api in API_SOURCES:
        try:
            url = api.format(domain=domain)
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):  # crt.sh
                    for entry in data:
                        subdomains.add(entry['name_value'])
                elif 'passive_dns' in data:
                    for record in data['passive_dns']:
                        subdomains.add(record['hostname'])
                elif 'subdomains' in data:
                    subdomains.update(data['subdomains'])
        except:
            continue
    
    # Print OSINT results in real-time
    for sub in sorted(subdomains):
        print(f"🌍 [OSINT] ✅ {sub}")
    
    return subdomains

# Brute-force Subdomains (Handles Empty Lines)
def brute_force_subdomains(domain, wordlist):
    subdomains = set()
    print(f"\n🚀 Starting brute-force scan for {domain}...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_subdomain = {
            executor.submit(is_active, f"{sub.strip()}.{domain}"): f"{sub.strip()}.{domain}"
            for sub in wordlist if sub.strip()  # Skip empty lines
        }
        for future in concurrent.futures.as_completed(future_to_subdomain):
            subdomain = future_to_subdomain[future]
            if future.result():
                subdomains.add(subdomain)
                print(f"🔹 [LIVE] ✅ {subdomain}")  # Print result immediately
    
    return subdomains

# Main function for ZenScan integration
def subdomain_enumeration(domain, mode, custom_wordlist=None):
    print(f"\n🔎 Enumerating subdomains for: {domain}\n")
    all_subdomains = set()

    if mode == "1":
        osint_results = fetch_subdomains_from_apis(domain)
        all_subdomains.update(osint_results)

        brute_results = brute_force_subdomains(domain, DEFAULT_WORDLIST)
        all_subdomains.update(brute_results)

    elif mode == "2" and custom_wordlist:
        if not os.path.isfile(custom_wordlist):
            print("❌ Invalid wordlist path! Please enter a valid file.")
            sys.exit(1)

        with open(custom_wordlist, "r") as file:
            wordlist = [line.strip() for line in file if line.strip()]  # Remove empty lines

        print(f"📂 Using custom wordlist with {len(wordlist)} entries...\n")
        custom_results = brute_force_subdomains(domain, wordlist)
        all_subdomains.update(custom_results)

    else:
        print("❌ Invalid choice! Please select a valid option.")
        sys.exit(1)

    print("\n🎯 Subdomain Enumeration Completed!")
    return all_subdomains

# Function to integrate with start.py
def run_subdomain_scan(domain):
    print("\n" + "="*50)
    print(" 🔎 ZenScan - Subdomain Enumeration")
    print("="*50)
    print("\nSelect scanning mode:")
    print("1️⃣ OSINT API + Default Dictionary")
    print("2️⃣ Custom Wordlist Brute-force")

    choice = input("Enter option (1 or 2): ").strip()

    if choice == "1":
        subdomain_enumeration(domain, "1")
    elif choice == "2":
        custom_list = input("Enter path to your wordlist file: ").strip()
        subdomain_enumeration(domain, "2", custom_list)
    else:
        print("❌ Invalid choice! Exiting.")
        sys.exit(1)

# Script Execution
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python subdomain_scan.py <domain>")
        sys.exit(1)

    target_domain = sys.argv[1]
    run_subdomain_scan(target_domain)
