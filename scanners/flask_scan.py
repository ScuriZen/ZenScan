import requests

def run_flask_scan(target):
    response = requests.get(target)
    if "flask" in response.text.lower():
        print("[+] Flask application detected!")
