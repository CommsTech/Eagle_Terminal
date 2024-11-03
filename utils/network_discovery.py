import concurrent.futures
import ipaddress
import socket
import threading
from typing import Dict, List


def parse_ip_range(start_ip: str, end_ip: str = None) -> List[str]:
    if end_ip:
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        return [
            str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)
        ]
    else:
        return [str(ip) for ip in ipaddress.IPv4Network(start_ip, strict=False)]


def scan_single_ip(ip: str) -> Dict[str, str]:
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return {"hostname": hostname, "ip": ip}
    except socket.herror:
        return {"hostname": "Unknown", "ip": ip}


def scan_network(ip_list: List[str]) -> List[Dict[str, str]]:
    discovered_devices = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(scan_single_ip, ip): ip for ip in ip_list}
        for future in concurrent.futures.as_completed(future_to_ip):
            result = future.result()
            if result["hostname"] != "Unknown":
                discovered_devices.append(result)
    return discovered_devices


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("9.9.9.9", 80))
        return s.getsockname()[0]
    finally:
        s.close()
