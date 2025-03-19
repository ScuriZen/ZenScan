import requests
import dns.resolver
import concurrent.futures
import sys
import json
import os
from urllib.parse import urlparse


API_SOURCES = [
    "https://crt.sh/?q=%.{domain}&output=json",
    "https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns",
    "https://api.threatminer.org/v2/domain.php?q={domain}&rt=5",
    "https://sonar.omnisint.io/subdomains/{domain}"
]


DEFAULT_SUBDOMAIN_WORDLIST = [
    "admin", "mail", "ftp", "test", "dev", "staging", "api", "secure",
    "portal", "beta", "edge", "dashboard", "vpn", "office", "sso"
]


def generate_subdomain_variations(domain):
    prefixes = ["dev", "stg", "qa", "beta", "uat"]
    return [f"{p}.{domain}" for p in prefixes]


def is_active(subdomain):
    try:
        dns.resolver.resolve(subdomain, 'A')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout):
        return False


def fetch_subdomains_from_apis(domain):
    subdomains = set()
    for api in API_SOURCES:
        try:
            url = api.format(domain=domain)
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):  # For crt.sh
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

def load_custom_wordlist(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    else:
        print("❌ File not found! Using default wordlist.")
        return DEFAULT_SUBDOMAIN_WORDLIST


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

def run_subdomain_scan(domain):
    print("\n" + "="*50)
    print(f" 🔎 ZenScan - Subdomain Enumeration")
    print("="*50)
    
    print(f"\n🌍 Target: {domain}")


    api_results = fetch_subdomains_from_apis(domain)
    print(f"🌐 Found {len(api_results)} subdomains from OSINT sources")


    print("\n[1] Use Default Dictionary")
    print("[2] Provide Custom Dictionary Path")
    choice = input("\nEnter your choice: ")

    if choice == "2":
        file_path = input("📂 Enter dictionary file path: ")
        wordlist = load_custom_wordlist(file_path)
    else:
        wordlist = DEFAULT_SUBDOMAIN_WORDLIST

    brute_results = brute_force_subdomains(domain, wordlist)
    print(f"🔍 Found {len(brute_results)} subdomains from brute-force")

  
    wildcard_results = set(generate_subdomain_variations(domain))
    print(f"✨ Found {len(wildcard_results)} wildcard variations")


    all_subdomains = api_results.union(brute_results).union(wildcard_results)

 
    print("\n📌 Discovered Subdomains:\n")
    for sub in sorted(all_subdomains):
        print(f"✅ {sub}")

    print("\n🎯 Subdomain Enumeration Completed!")
    print("="*50)

    return all_subdomains

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python subdomain_scan.py <domain>")
        sys.exit(1)

    target_domain = sys.argv[1]
    run_subdomain_scan(target_domain)
