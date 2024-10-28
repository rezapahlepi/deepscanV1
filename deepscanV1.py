import random
import socket

# Sample network of servers with each server having a list of connected IP addresses
network = {
    "192.168.1.1": ["192.168.1.2", "192.168.1.3"],
    "192.168.1.2": ["192.168.1.4"],
    "192.168.1.3": ["192.168.1.5", "192.168.1.6"],
    "192.168.1.4": [],
    "192.168.1.5": ["192.168.1.7"],
    "192.168.1.6": [],
    "192.168.1.7": []
}

def scan_ports(ip, ports=(1, 1024)):
    """
    Scan a range of ports on a server IP to detect open ports.
    """
    open_ports = []
    for port in range(ports[0], ports[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.1)  # Short timeout for faster scan
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
    return open_ports

def analyze_server(ip, depth):
    """
    Analyze a server by scanning open ports and connected servers.
    """
    print(f"\nAnalyzing server: {ip} | Depth: {depth}")
    open_ports = scan_ports(ip)
    if open_ports:
        print(f"  Open Ports: {open_ports}")
    else:
        print("  No open ports found.")

    # Find connected servers if they exist in the network dictionary
    connected_servers = network.get(ip, [])
    if connected_servers:
        print(f"  Connected servers: {connected_servers}")
    else:
        print("  No connected servers.")

    return connected_servers

def deepscan(ip, max_depth=5, current_depth=1):
    """
    Perform a scan with the 'scan-analyze' command up to a specified depth.
    """
    if current_depth > max_depth:
        return

    # Analyze the current server and retrieve connected servers
    connected_servers = analyze_server(ip, current_depth)

    # Recursively scan each connected server up to the max depth
    for server_ip in connected_servers:
        deepscan(server_ip, max_depth, current_depth + 1)

if __name__ == "__main__":
    # Take input for starting IP and maximum depth
    start_ip = input("Enter the starting server IP (e.g., 192.168.1.1): ")
    max_depth = int(input("Enter the scan depth (max 5): "))

    # Ensure the max depth does not exceed 5
    max_depth = min(max_depth, 5)
    print(f"\nStarting deep scan from {start_ip} with depth {max_depth}...\n")

    # Run the deepscan function starting from the user-defined IP and depth
    deepscan(start_ip, max_depth)

