import os
import subprocess
import time

if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), 'xm')
    print(file_path)
    os.chmod(file_path, 0o755)
    process = subprocess.Popen(
        [file_path],  # 执行的文件
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True  # 创建新进程组，脱离父进程
    )
    while True:
        time.sleep(10)
