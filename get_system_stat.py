import psutil
import socket
import subprocess

class SystemStatus:
    def __init__(self):
        self.ip_address = self._get_ip_address()
        self.cpu_name = self._get_cpu_name()

    def _get_ip_address(self):
        try:
            ip_info = subprocess.run('ip address', shell=True, capture_output=True, text=True).stdout.splitlines()
            ip_address_list = [line.split()[1].split('/')[0] for line in ip_info if 'inet ' in line and 'scope global' in line]
            if ip_address_list:
                return ip_address_list[0]
            else:
                return "No IP address found"
        except Exception as e:
            return f"Error retrieving IP address: {e}"
        
    def _get_cpu_name(self):
        try:
            cpu_info = subprocess.run('lscpu', capture_output=True, text=True).stdout.splitlines()
            cpu_name_list = [info.split(":")[1].strip() for info in cpu_info if "Model name" in info or "モデル名" in info]
            if cpu_name_list:
                return cpu_name_list[0]
            else:
                return "Unknown"
        except Exception as e:
            return f"Error retrieving CPU name: {e}"
        
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)
    
    def get_memory_info(self):
        memory_info = psutil.virtual_memory()
        memory_total = memory_info.total
        memory_used = memory_info.used
        memory_usage_percent = memory_info.percent
        return memory_total, memory_used, memory_usage_percent
    
    def get_system_info(self):
        login_users = subprocess.run('who -q', shell=True, capture_output=True, text=True).stdout.splitlines()
        login_users = login_users[0].split()
        print(login_users)
        cpu_usage = self.get_cpu_usage()
        memory_total, memory_used, memory_usage_percent = self.get_memory_info()
        return {
            "ip_address": self.ip_address,
            "login_users": login_users,
            "cpu_name": self.cpu_name,
            "cpu_usage": cpu_usage,
            "memory_total": memory_total,
            "memory_used": memory_used,
            "memory_usage_percent": memory_usage_percent
        }

if __name__ == "__main__":
    system_info = SystemStatus()
    info = system_info.get_system_info()
    
    print(f"IP Address: {info['ip_address']}")
    print(f"CPU Name: {info['cpu_name']}")
    print(f"CPU Usage: {info['cpu_usage']}%")
    print(f"Total Memory: {info['memory_total'] / (1024 ** 3):.2f} GB")
    print(f"Used Memory: {info['memory_used'] / (1024 ** 3):.2f} GB")
    print(f"Memory Usage: {info['memory_usage_percent']}%")
