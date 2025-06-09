import os
import subprocess
import streamlit as st
# 文件名
file_name = "xm"

# 获取文件路径
file_path = os.path.join(os.getcwd(), file_name)

# 赋予执行权限
os.chmod(file_path, 0o755)

# 使用 Popen 执行文件并持续读取输出
try:
    # 启动子进程
    process = subprocess.Popen(
        [file_path],  # 执行的文件
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,  # 捕获错误输出
        text=True,  # 输出以文本方式返回
        bufsize=1,  # 逐行刷新缓冲区
        universal_newlines=True  # 确保输出是字符串形式
    )

    print("执行中，输出内容如下喵～：")

    # 持续读取标准输出
    for line in process.stdout:
        st.write(line.strip())  # 去除换行符并打印

    # 检查是否有错误输出
    stderr = process.stderr.read()
    if stderr:
        print("错误信息喵～：")
        print(stderr)

    # 等待进程结束
    process.wait()
    print(f"执行完成，退出码：{process.returncode}")
except Exception as e:
    print(f"执行失败啦~喵！原因: {e}")
