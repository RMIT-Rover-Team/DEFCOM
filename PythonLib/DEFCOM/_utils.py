import socket
import psutil

def _isMyIP(Host: str):
    for iface, addrs in psutil.net_if_addrs().items():
        for a in addrs:
            if a.family in (socket.AF_INET, socket.AF_INET6):
                # Normalize IPv6 (strip %scope)
                addr = a.address.split('%')[0]
                if addr == Host:
                    return True
    return False