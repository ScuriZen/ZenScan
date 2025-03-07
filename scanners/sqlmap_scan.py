import os

def run_sqlmap_scan(target):
    print(f"\n\033[91m[+] Running SQL Injection scan on {target} using sqlmap...\033[0m\n")
    output = os.popen(f"sqlmap -u {target} --dbs --batch").read()
    return output  # Return results
