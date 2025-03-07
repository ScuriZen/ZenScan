import nmap

def run_nmap_scan(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, arguments="-sV -Pn")
    return scanner.all_hosts()
