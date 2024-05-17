import subprocess


class GPUStatus:
    
    def __init__(self, keys=None, no_units=False):
        self.keys = keys or [
            "index",
            "gpu_name",
            "memory.total",
            "memory.used",
            "utilization.gpu",
            "utilization.memory",
            "temperature.gpu",
        ]
        self.no_units = no_units

    def get_gpu_info(self):
        queries = ",".join(self.keys)
        output_fmt = "csv,noheader"
        if self.no_units:
            output_fmt += ",nounits"

        cmd = f"nvidia-smi --query-gpu={queries} --format={output_fmt}"
        output = subprocess.check_output(cmd, shell=True).decode()
        output = output.replace(", ", ",")  # カンマの後の空白を削除する

        lines = output.strip().split('\n')
        gpu_info_list = []

        for line in lines:
            values = line.split(',')
            gpu_info = {key: value for key, value in zip(self.keys, values)}
            gpu_info_list.append(gpu_info)
        
        return gpu_info_list


# 使用例
if __name__ == "__main__":
    gpu_status = GPUStatus()
    info = gpu_status.get_gpu_info()
    
    for gpu in info:
        print(f"GPU Index: {gpu['index']}")
        print(f"GPU Name: {gpu['gpu_name']}")
        print(f"Memory Total: {gpu['memory.total']} MiB")
        print(f"Memory Used: {gpu['memory.used']} MiB")
        print(f"GPU Utilization: {gpu['utilization.gpu']} %")
        print(f"Memory Utilization: {gpu['utilization.memory']} %")
        print(f"GPU Temperature: {gpu['temperature.gpu']} C")
        print()
