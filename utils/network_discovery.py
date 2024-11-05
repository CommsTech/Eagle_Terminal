import concurrent.futures
import ipaddress
import socket
import threading
from typing import Dict, List


def parse_ip_range(start_ip: str, end_ip: str = None) -> List[str]:
    """Parse a range of IP addresses.
    
    Args:
        start_ip str: The starting IP address of the range, or a CIDR notation if end_ip is not provided.
        end_ip str: Optional. The ending IP address of the range.
    
    Returns:
        List[str]: A list of IP addresses as strings within the specified range.
    
    Raises:
        ValueError: If the IP addresses are invalid or if the range is incorrect.
    """
    if end_ip:
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        return [
            str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)
        ]
    else:
        return [str(ip) for ip in ipaddress.IPv4Network(start_ip, strict=False)]


def scan_single_ip(ip: str) -> Dict[str, str]:
    """Performs a reverse DNS lookup for a given IP address.
    
    Args:
        ip (str): The IP address to perform the reverse DNS lookup on.
    
    Returns:
        Dict[str, str]: A dictionary containing the hostname and IP address.
                        If the hostname cannot be resolved, 'Unknown' is returned as the hostname.
    
    Raises:
        socket.herror: This exception is caught internally and does not propagate.
    """
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return {"hostname": hostname, "ip": ip}
    except socket.herror:
        return {"hostname": "Unknown", "ip": ip}


def scan_network(ip_list: List[str]) -> List[Dict[str, str]]:
    """Scans a list of IP addresses concurrently to discover network devices.
    
    Args:
        ip_list List[str]: A list of IP addresses to scan.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries containing information about discovered devices.
                              Each dictionary includes details such as IP address and hostname.
    """
    discovered_devices = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(scan_single_ip, ip): ip for ip in ip_list}
        for future in concurrent.futures.as_completed(future_to_ip):
            result = future.result()
            if result["hostname"] != "Unknown":
                discovered_devices.append(result)
    return discovered_devices


def get_local_ip() -> str:
    """Retrieves the local IP address of the machine.
    
    Returns:
        str: The local IP address as a string.
    
    Raises:
        socket.error: If there's an error creating or using the socket.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("9.9.9.9", 80))
        return s.getsockname()[0]
    finally:
        s.close()
