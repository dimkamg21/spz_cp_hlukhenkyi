import netifaces
import subprocess

class NetworkMonitor:
    def __init__(self, root, network_gui=None):
        self.root = root
        self.network_gui = network_gui

    def get_dns_servers(self):
        dns_servers = []
        try:
            result = subprocess.check_output("ipconfig /all", shell=True).decode()
            for line in result.splitlines():
                if "DNS Servers" in line:
                    dns_servers.append(line.split(":")[1].strip())
        except Exception as e:
            self.logger.log_info(f"Error retrieving DNS servers: {e}")
        return dns_servers

    def is_dhcp_enabled(self, interface):
        try:
            result = subprocess.check_output(f"netsh interface ip show config name=\"{interface}\"", shell=True).decode()
            if "DHCP enabled: Yes" in result:
                return True
        except subprocess.CalledProcessError as e:
            self.logger.log_info(f"Error checking DHCP: {e}")
        return False

    def get_network_info(self):
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                ip_info = addrs[netifaces.AF_INET][0]
                ip_address = ip_info.get('addr')
                netmask = ip_info.get('netmask')
                gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
                mac_address = addrs[netifaces.AF_LINK][0].get('addr')
                dns_servers = self.get_dns_servers()
                dhcp_enabled = self.is_dhcp_enabled(interface)
                active_interface_name = interface

                if interface == "{D9E46C1E-EFA5-40D1-8D96-D14FFDE97298}":
                    active_interface_name = "Ethernet"

                return {
                    'interface':  active_interface_name,
                    'mac_address': mac_address,
                    'ip_address': ip_address,
                    'gateway': gateway,
                    'netmask': netmask,
                    'dns_servers': dns_servers,
                    'dhcp_enabled': dhcp_enabled,
                }
        return {}

    
