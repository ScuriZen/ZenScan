import ipaddress
import concurrent.futures
import os
import subprocess
import re
import socket
from mac_vendor_lookup import MacLookup

mac = MacLookup()


def get_mac(ip):
    """Retrieve MAC address using ARP command."""
    try:
        arp_output = subprocess.check_output(["arp", "-a", ip], stderr=subprocess.DEVNULL, text=True)
        mac_match = re.search(r"(([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2})", arp_output)
        if mac_match:
            return mac_match.group(0)
    except Exception:
        pass
    return None


def get_mac_and_vendor(ip):
    """Retrieve MAC and vendor for the IP."""
    mac_address = get_mac(ip)
    vendor = mac.lookup(mac_address) if mac_address else "Unknown"
    return mac_address, vendor


def get_hostname(ip):
    """Resolve hostname of the IP."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""


def get_os_info(ip):
    """(Stub) Try to guess OS using TTL values (requires root or advanced scan)."""
    # Advanced: Could use scapy or Nmap OS scan
    return "Unknown"


def is_ip_active(ip):
    """Check if IP is alive using ARP or ping."""
    if get_mac(ip):
        return ip
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            return ip
    except Exception:
        pass
    return None


def identify_device(vendor):
    """Guess device type based on vendor name."""
    vendor = vendor.lower()
    if "apple" in vendor:
        return "iPhone/MacBook"
    elif "samsung" in vendor:
        return "Samsung Phone"
    elif "xiaomi" in vendor or "redmi" in vendor:
        return "Xiaomi Phone"
    elif "huawei" in vendor:
        return "Huawei Phone"
    elif "cisco" in vendor:
        return "Router/Switch"
    elif "tp-link" in vendor:
        return "Router"
    elif "netgear" in vendor:
        return "Router"
    elif "dell" in vendor or "hp" in vendor or "lenovo" in vendor:
        return "Laptop"
    elif "canon" in vendor or "epson" in vendor:
        return "Printer"
    elif "hikvision" in vendor or "dahua" in vendor:
        return "CCTV Camera"
    elif "fortinet" in vendor or "palo alto" in vendor or "checkpoint" in vendor:
        return "Firewall"
    elif "raspberry" in vendor:
        return "Raspberry Pi"
    elif "chongqing fugui" in vendor:
        return "laptop (OEM Apple Manufacturer)"
    else:
        return "Unknown Device"


def scan_ip_range(start_ip, end_ip):
    """Scan IPs in given range and return details of active devices."""
    print(f"\n🚀 Scanning IP range: {start_ip} - {end_ip}...\n")

    active_devices = []
    seen_ips = set()

    # Generate IPs from range
    ips = []
    for net in ipaddress.summarize_address_range(ipaddress.IPv4Address(start_ip),
                                                 ipaddress.IPv4Address(end_ip)):
        ips.extend([str(ip) for ip in net.hosts()
                    if not (str(ip).endswith('.0') or str(ip).endswith('.255'))])

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(is_ip_active, ip): ip for ip in ips}
        for future in concurrent.futures.as_completed(futures):
            ip = future.result()
            if ip and ip not in seen_ips:
                seen_ips.add(ip)
                mac_address, vendor = get_mac_and_vendor(ip)
                device_type = identify_device(vendor)
                hostname = get_hostname(ip)
                os_info = get_os_info(ip)

                # Get brand from hostname if available, otherwise use 'Unknown'
                brand = hostname.split('.')[0] if hostname else "Unknown"

                print(f"""✅ [LIVE]
🌐 IP: {ip}
🔍 MAC: {mac_address}
🏭 Vendor: {vendor}
🏷️ Brand: {brand}
🖥️ Device Type: {device_type}
🧠 OS: {os_info}
🔠 Hostname: {hostname}
""")
                active_devices.append((ip, vendor, device_type, os_info, mac_address, hostname))

    print("🎯 Scan Complete!")
    return active_devices


def start_ip_scan():
    start_ip = input("Enter start IP: ").strip()
    end_ip = input("Enter end IP: ").strip()
    scan_ip_range(start_ip, end_ip)
  
if __name__ == "__main__":
    start_ip_scan()
                                        
