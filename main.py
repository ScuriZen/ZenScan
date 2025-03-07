import argparse
from scanners.nmap_scan import run_nmap_scan
from scanners.sqlmap_scan import run_sqlmap_scan
from scanners.wapiti_scan import run_wapiti_scan
from scanners.flask_scan import run_flask_scan

def main():
    parser = argparse.ArgumentParser(description="ZenScan - Multi-Tool Security Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target domain or IP")
    parser.add_argument("-m", "--mode", choices=["nmap", "sqlmap", "wapiti", "flask"], help="Scanner mode")
    
    args = parser.parse_args()
    
    if args.mode == "nmap":
        print("[+] Running Nmap scan...")
        print(run_nmap_scan(args.target))
    
    elif args.mode == "sqlmap":
        print("[+] Running SQLMap scan...")
        run_sqlmap_scan(args.target)

    elif args.mode == "wapiti":
        print("[+] Running Wapiti scan...")
        run_wapiti_scan(args.target)

    elif args.mode == "flask":
        print("[+] Running Flask vulnerability scan...")
        run_flask_scan(args.target)

if __name__ == "__main__":
    main()
