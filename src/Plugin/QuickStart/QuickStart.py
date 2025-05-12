
import subprocess


def execute_command(parameter):
    try:
        subprocess.Popen(parameter)
    except Exception as err:
        print(f"执行命令出错: {str(err)}")
