def ip_to_int(ip: str) -> int:
    ip_parts = ip.split(".")
    parts = len(ip_parts)
    ip_int = 0
    for i in range(parts):
        ip_int |= int(ip_parts[i]) << (8 * (parts - 1 - i))
    return ip_int
