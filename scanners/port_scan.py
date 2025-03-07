import socket

def run_port_scan(target):
    print(f"\n\033[94m[+] Scanning open ports on {target}...\033[0m\n")
    common_ports = [21, 22, 23, 25, 53, 80, 443, 8080]
    result = ""

    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result_code = sock.connect_ex((target, port))
        if result_code == 0:
            result += f"✔ Port {port} is \033[92mOPEN\033[0m\n"
        else:
            result += f"✘ Port {port} is \033[91mCLOSED\033[0m\n"
        sock.close()

    return result  # Returning output

