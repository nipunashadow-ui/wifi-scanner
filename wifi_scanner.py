import socket
import subprocess
import platform
import re
import ipaddress
import urllib.request
import urllib.error
import time
from concurrent.futures import ThreadPoolExecutor

def get_my_ip():
    """Step 1: Find this computer's own IP address on the local network."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"

def get_subnet_ips(my_ip):
    """Step 2: Generate a list of all IP addresses in the /24 network."""
    network = ipaddress.ip_network(f"{my_ip}/24", strict=False)
    return [str(ip) for ip in network.hosts()]

def ping_ip(ip):
    """Sends a single ping to an IP address to wake it up."""
    if platform.system().lower() == "windows":
        command = ["ping", "-n", "1", "-w", "500", ip]
    else:
        command = ["ping", "-c", "1", "-W", "1", ip]

    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def ping_sweep(ip_list):
    """Step 3: Ping every address in the subnet at the same time."""
    print(f"[*] Pinging {len(ip_list)} addresses, please wait...")
    with ThreadPoolExecutor(max_workers=100) as pool:
        pool.map(ping_ip, ip_list)

def read_arp_table():
    """Step 4: Read the OS ARP table to map IPs to MAC addresses."""
    devices = {}
    try:
        output = subprocess.check_output(["arp", "-a"], text=True, errors="ignore")
    except Exception as e:
        print(f"[!] Error reading ARP table: {e}")
        return devices

    ip_pattern = r"(\d{1,3}(?:\.\d{1,3}){3})"
    mac_pattern = r"([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}"

    for line in output.splitlines():
        ip_match = re.search(ip_pattern, line)
        mac_match = re.search(mac_pattern, line)

        if ip_match and mac_match:
            ip = ip_match.group(0)
            mac = mac_match.group(0).lower().replace("-", ":")
            
            if not mac.startswith(("ff:ff", "01:00", "33:33")) and mac != "00:00:00:00:00:00":
                devices[ip] = mac

    return devices

def get_vendor(mac):
    """Guess the device maker from its MAC address using a free API."""
    # Check if the device is using a randomized/private MAC address
    if len(mac) >= 2 and mac[1] in ['2', '6', 'a', 'e']:
        return "Randomized (Private MAC)"

    # Use macvendors.com API
    url = f"https://api.macvendors.com/{mac}"
    
    try:
        # We add a generic User-Agent so the API doesn't block the Python script
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            vendor = response.read().decode('utf-8')
            
            # The free API limits requests to 1 per second. 
            # We sleep for half a second to prevent getting temporarily blocked.
            time.sleep(0.5) 
            return vendor
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "Unknown Vendor"
        elif e.code == 429:
            return "Rate Limited (Too fast)"
        return f"API Error {e.code}"
    except Exception:
        return "Lookup Failed"

def get_hostname(ip):
    """Try to find the device's hostname via reverse DNS."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""

def main():
    """Main execution block."""
    print("=" * 70)
    print(" Wi-Fi Network Scanner (API Edition)")
    print(" Scan networks you own or are allowed to use!")
    print("=" * 70)

    my_ip = get_my_ip()
    print(f"[*] My IP address : {my_ip}")

    ip_list = get_subnet_ips(my_ip)
    ping_sweep(ip_list)

    devices = read_arp_table()
    print(f"[*] Found {len(devices)} device(s) on the network.\n")

    print(f"{'IP Address':<16} {'MAC Address':<19} {'Vendor':<25} Hostname")
    print("-" * 80)

    sorted_ips = sorted(devices.keys(), key=lambda ip: ipaddress.IPv4Address(ip))

    for ip in sorted_ips:
        mac = devices[ip]
        hostname = get_hostname(ip)
        
        # We fetch the vendor here. It might take a moment per device due to the API.
        vendor = get_vendor(mac)
        
        vendor_display = vendor[:23] + ".." if len(vendor) > 25 else vendor
        print(f"{ip:<16} {mac:<19} {vendor_display:<25} {hostname}")

    print("-" * 80)

if __name__ == "__main__":
    main()