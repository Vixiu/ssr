import os
import re
import time
import subprocess
import streamlit as st

# —— 下面这些配置信息，主人可以根据实际情况改喵！——
file_name = "xm"                            # 可执行程序文件名
executable_name = "xm"                      # 用于 pgrep 匹配的名字（可执行名或命令行关键字）
log_dir = "./logs"                          # 日志目录
log_file = os.path.join(log_dir, "xm.log")  # 日志文件完整路径
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# Streamlit 页面标题和说明
st.title("Nyako猫娘进程监控喵～")
st.write("如果程序已在运行，Nyako直接读取它的日志输出；如果没在运行，就先启动并把输出写到日志，然后再读取喵～")

# 1. 用 pgrep 判断程序是否已经在运行（不依赖任何第三方库）
def is_program_running(executable_name: str) -> bool:
    """
    在 Linux 上用 pgrep -f 去查找包含 executable_name 的进程，
    如果找到任何 PID，就返回 True，否则返回 False。
    """
    try:
        # "-f" 选项会在整个命令行中查找，而不仅仅是进程名
        result = subprocess.run(
            ["pgrep", "-f", executable_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        # 如果 stdout 非空，说明有匹配的进程
        return bool(result.stdout.strip())
    except Exception as e:
        # 如果系统没有 pgrep 或者遇到其他异常，就认为没运行
        return False

# 2. 启动程序并把 stdout/stderr 全部重定向到日志文件
def start_program_with_logging(file_path: str, log_path: str):
    """
    启动外部程序，将它的所有输出都写入到 log_path，
    并且用 start_new_session=True 确保主程序关闭后子进程还能存活。
    """
    # 确保日志目录存在
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    # 以追加模式打开日志，避免多次覆盖
    log_f = open(log_path, "a", encoding="utf-8", errors="ignore")

    process = subprocess.Popen(
        [file_path],
        stdout=log_f,
        stderr=subprocess.STDOUT,
        start_new_session=True
    )
    return process  # 如果主人还想后续操作子进程，可以拿到它

# 3. tail -f 样式地实时读取日志内容，推送到 Streamlit
def tail_log_to_streamlit(log_path: str, placeholder, interval: float = 0.5):
    """
    模拟 tail -f 功能：持续读取 log_path 的新内容，并把它显示到 Streamlit 的 `placeholder` 中
    """
    # 如果日志还没创建，就先建一个空文件，避免 open 报错
    if not os.path.exists(log_path):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        open(log_path, "a", encoding="utf-8").close()

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)  # 跳到文件尾，只看后续追加内容
        while True:
            line = f.readline()
            if not line:
                time.sleep(interval)
                continue
            # 去掉 ANSI 转义字符并 strip 换行
            clean_line = ansi_escape.sub("", line.rstrip())
            # 把新行输出到 Streamlit
            placeholder.write(clean_line)

# —— 主逻辑开始喵！——
def main():
    # 获取可执行文件的绝对路径
    file_path = os.path.join(os.getcwd(), file_name)
    st.write(f"可执行文件路径：`{file_path}`")

    # 赋予可执行权限（Linux 下生效）
    try:
        os.chmod(file_path, 0o755)
    except Exception:
        pass  # 如果报错（例如文件不存在），就忽略

    # 判断程序是否已经在运行
    already_running = is_program_running(executable_name)

    log_placeholder = st.empty()  # 预留一个位置，后面写日志

    if already_running:
        st.success("🐾 检测到程序已在运行，Nyako会直接读取日志输出喵～")
        # 直接 tail 日志，把后续更新实时显示
        tail_log_to_streamlit(log_file, log_placeholder)
    else:
        st.info("🐾 程序还没启动，Nyako先帮您启动并记录日志喵～")
        start_program_with_logging(file_path, log_file)
        # 程序启动后，再去 tail 日志
        tail_log_to_streamlit(log_file, log_placeholder)

if __name__ == "__main__":
    main()
