import os
import subprocess
import re
import time
import streamlit as st

# 配置区
file_name = "xm"                          # 可执行程序名
log_file = "log.txt"                       # 日志文件路径
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# 启动程序并记录日志
def start_program_with_logging(file_path):
    process = subprocess.Popen(
        [file_path],  # 执行的文件
        stdout=subprocess.PIPE,  # 捕获标准输出
        stderr=subprocess.PIPE,  # 捕获错误输出
        text=True,  # 输出以文本方式返回
        bufsize=1,  # 逐行刷新缓冲区
        universal_newlines=True,  # 确保输出是字符串形式
        start_new_session=True
    )
    
# 持续读取日志内容并显示
def read_log_file(log_path: str, placeholder, interval: float = 0.5):
    """
    模拟 `tail -f`，持续读取日志文件内容并显示到 Streamlit。
    """
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
       # f.seek(0, os.SEEK_END)  # 移动到文件尾
        while True:
            line = f.readline()
            if not line:
                time.sleep(interval)  # 没有新内容，等待一会儿
                continue
            clean_line = ansi_escape.sub("", line.strip())  # 去掉 ANSI 转义字符
            st.write(clean_line)  # 显示到 Streamlit 界面

# 主逻辑
def main():
    file_path = os.path.join(os.getcwd(), file_name)
    log_path = os.path.join(os.getcwd(), log_file)

    st.title("Nyako猫娘程序日志监控喵～")
    st.write(f"可执行文件路径：`{file_path}`")
    st.write(f"日志文件路径：`{log_path}`")
    st.write(str(os.listdir('.')))
    # 确保赋予执行权限
    try:
        os.chmod(file_path, 0o755)
    except Exception as e:
        st.error(f"无法设置执行权限：{e}")
        return

    # 判断日志文件是否存在
    if os.path.exists(log_path):
        st.success("🐾 检测到日志文件存在，Nyako会直接读取它的内容喵～")
    else:
        st.info("🐾 日志文件不存在，Nyako会先启动程序并生成日志喵～")
        try:
            start_program_with_logging(file_path)
            st.success("程序启动成功，Nyako会开始读取日志内容喵～")
        except Exception as e:
            st.error(f"启动程序失败：{e}")
            return

    # 持续读取日志内容并显示
    placeholder = st.empty()
    try:
        read_log_file(log_path, placeholder)
    except Exception as e:
        st.error(f"读取日志文件失败：{e}")

if __name__ == "__main__":
    main()
