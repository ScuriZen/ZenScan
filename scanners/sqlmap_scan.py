import os

def run_sqlmap_scan(target):
    print(f"Running SQL Injection scan on {target} using sqlmap...\n")
    os.system(f"sqlmap -u {target} --dbs --batch")

