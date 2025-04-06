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
    """Retrieve MAC address and vendor using mac-vendor-lookup and fallback to prefix map."""
    mac_address = get_mac(ip)
    vendor = "Unknown"

    if mac_address:
        try:
            vendor = mac.lookup(mac_address)
        except Exception:
            # fallback to hardcoded prefix lookup
            prefix = mac_address.upper().replace(":", "").replace("-", "")[:6]

            vendor_prefixes = {
                "D8BB2C": "Apple", "F0D5BF": "Apple", "3C0754": "Apple", "A4B121": "Apple", "90B21F": "Apple",
                "BC83A7": "Samsung", "60D819": "Samsung", "0026C7": "Samsung", "1CB72C": "Samsung", "6CB7F4": "Samsung",
                "60EB69": "Xiaomi", "A0F3C1": "Xiaomi", "3C5A37": "Xiaomi", "B0E235": "Xiaomi", "48A9D2": "Xiaomi",
                "A0B4A5": "Huawei", "FCAA14": "Huawei", "30F335": "Huawei", "84A466": "Huawei", "C4AD34": "Huawei",
                "3C57D5": "TP-Link", "FCFC48": "TP-Link", "30B5C2": "TP-Link", "647002": "TP-Link", "50984B": "TP-Link",
                "FCF5C4": "Netgear", "A02BB8": "Netgear", "28C68E": "Netgear", "001E2A": "Netgear", "0026F2": "Netgear",
                "D067E5": "Dell", "C8D3A3": "Dell", "1C697A": "Dell", "F8BC12": "Dell", "F0F1A9": "Dell",
                "0026B6": "Canon", "B8B5AF": "Canon", "089E08": "Canon", "0021E9": "Canon",
                "AC9B0A": "Hikvision", "D4AE52": "Hikvision", "64A837": "Hikvision",
                "000C29": "VMware", "000569": "VMware", "005056": "VMware",
                "DC44B6": "Raspberry Pi", "B827EB": "Raspberry Pi", "E45F01": "Raspberry Pi",
                "00000C": "Cisco", "F8E71E": "Cisco", "705AB6": "Cisco",
                "3C970E": "Intel", "F0DE71": "Intel", "A0369F": "Intel",
                "1C7508": "HP", "B4B52F": "HP", "B0A8B9": "HP",
                "F8A45F": "Asus", "14D6XX": "Asus", "74D435": "Asus",
                "041E64": "Lenovo", "28D244": "Lenovo", "001EC9": "Lenovo",
            }

            vendor = vendor_prefixes.get(prefix, "Unknown")

    return mac_address, vendor



def get_hostname(ip):
    """Resolve hostname using DNS, fallback to nbtscan for NetBIOS name."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        try:
            output = subprocess.check_output(["nbtscan", "-s", ",", ip], stderr=subprocess.DEVNULL, text=True)
            lines = output.strip().splitlines()
            if len(lines) > 1:
                fields = lines[1].split(",")
                if len(fields) > 1:
                    return fields[1].strip()
        except Exception:
            pass
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


def run_ip_range(start_ip, end_ip):
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

                # Device Name / Brand logic
                device_name = hostname.split('.')[0] if hostname else "Unknown"

                print(f"""✅ [LIVE]
🌐 IP: {ip}
🔍 MAC: {mac_address}
🏭 Vendor: {vendor}
📛 Device Name: {device_name}
🖥️ Device Type: {device_type}
🧠 OS: {os_info}
🔠 Hostname: {hostname}
""")
                active_devices.append((ip, vendor, device_type, os_info, mac_address, hostname))

    print("🎯 Scan Complete!")
    return active_devices



def run_ip_scan():
    start_ip = input("Enter start IP: ").strip()
    end_ip = input("Enter end IP: ").strip()
    run_ip_range(start_ip, end_ip)
  
if __name__ == "__main__":
    run_ip_scan()
                                        
