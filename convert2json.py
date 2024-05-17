import get_system_stat
import get_gpu_stat
import json
import subprocess

class CombinedInfo:
    def __init__(self):
        self.system_stat = get_system_stat.SystemStatus()
        self.gpu_stat = get_gpu_stat.GPUStatus()

    
    def get_combined_info(self):
        # システム情報を取得
        system_info = self.system_stat.get_system_info()
        # GPU情報を取得
        gpu_info = self.gpu_stat.get_gpu_info()
        
        # 情報を結合する
        combined_info = {
            "System Info": {
                "IP Address": system_info["ip_address"],
                "Login Users": system_info["login_users"],
                "CPU Name": system_info["cpu_name"],
                "CPU Usage": f"{system_info['cpu_usage']}%",
                "Total Memory": f"{system_info['memory_total'] / (1024 ** 3):.2f} GB",
                "Used Memory": f"{system_info['memory_used'] / (1024 ** 3):.2f} GB",
                "Memory Usage": f"{system_info['memory_usage_percent']}%",
            },
            "GPU Status": []
        }
        
        for gpu in gpu_info:
            combined_info["GPU Status"].append({
                "GPU Index": gpu['index'],
                "GPU Name": gpu['gpu_name'],
                "Memory Total": gpu['memory.total'],
                "Memory Used": gpu['memory.used'],
                "GPU Utilization": gpu['utilization.gpu'],
                "Memory Utilization": gpu['utilization.memory'],
                "GPU Temperature": f"{gpu['temperature.gpu']} C",
            })
        
        return combined_info

    def save_to_json(self):
        try:
            ip_info = subprocess.run('ip address', shell=True, capture_output=True, text=True).stdout.splitlines()
            ip_address_list = [line.split()[1].split('/')[0] for line in ip_info if 'inet ' in line and 'scope global' in line]
            if ip_address_list:
                ip_address = ip_address_list[0]
            else:
                print("No IP address found")
        except Exception as e:
            print(f"Error retrieving IP address: {e}")
        filename = ip_address + ".json"
        combined_info = self.get_combined_info()
        # with open(filename, 'w') as json_file:
        #     json.dump(combined_info, json_file, indent=4)
        # print(f'JSONファイル {filename} に保存されました。')
        json_data = json.dumps(combined_info, indent=4)
        print('JSONデータを返します。')
        return json_data

if __name__ == "__main__":
    system_gpu_info = CombinedInfo()
    
    # JSON形式で表示
    combined_info = system_gpu_info.get_combined_info()
    print(json.dumps(combined_info, indent=4))
    
    # ファイルに保存
    ip_address = combined_info["System Info"]["IP Address"]
    system_gpu_info.save_to_json()
