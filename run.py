import os
import subprocess
import time

if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), 'xm')
    os.chmod(file_path, 0o755)
    process = subprocess.Popen(
        [file_path],  # 执行的文件
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,  # 捕获错误输出
        text=True  # 输出以文本方式返回
    )
    while True:
        time.sleep(10)
