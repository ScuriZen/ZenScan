import os

def run_sqlmap_scan(url):
    command = f"sqlmap -u {url} --batch --dbs"
    os.system(command)

