import os
import subprocess
import re
import time
import streamlit as st

# 配置区
file_name = "xm"  # 可执行程序名
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# 检查程序是否运行中
def is_program_running(process_name: str) -> bool:
    """
    使用 `pgrep` 检查是否有包含 `process_name` 的程序在运行。
    """
    try:
        result = subprocess.run(
            ["pgrep", "-f", process_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.returncode == 0
    except Exception as e:
        return False

# 启动程序
def start_program(file_path: str):
    """
    启动指定程序，并返回进程对象。
    """
    process = subprocess.Popen(
        [file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
        start_new_session=True,
    )
    return process

# 读取程序输出并实时显示
def read_process_output(process, placeholder):
    """
    从进程的标准输出实时读取内容并显示到 Streamlit。
    """
    for line in iter(process.stdout.readline, ''):
        clean_line = ansi_escape.sub("", line.strip())
        placeholder.write(clean_line)
    process.stdout.close()
    process.wait()

# 主逻辑
def main():
    file_path = os.path.join(os.getcwd(), file_name)
    st.write(f"可执行文件路径：`{file_path}`")
    
    # 确保赋予执行权限
    try:
        os.chmod(file_path, 0o755)
    except Exception as e:
        st.error(f"无法设置执行权限：{e}")
        return

    # 检查程序是否在运行
    if is_program_running(file_name):
        st.success("程序已在运行，直接连接到其输出喵～")
        st.warning("🐾 由于直接连接正在运行的程序较为复杂，目前暂时无法实现直接输出哦～")
    else:
        st.info("程序未运行，现在启动并读取输出喵～")
        try:
            process = start_program(file_path)
            placeholder = st.empty()
            read_process_output(process, placeholder)
        except Exception as e:
            st.error(f"启动或读取程序失败：{e}")

if __name__ == "__main__":
    main()
