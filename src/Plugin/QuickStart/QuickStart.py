
import subprocess

from src.Plugin.PluginBase import MenuPlugin


class QuickStartPlugin(MenuPlugin):
    """快速启动插件
    
    在系统托盘菜单中添加菜单项，点击菜单项执行相应命令
    支持自定义菜单功能
    """

    @staticmethod
    def execute_command(parameter):
        """执行命令
        
        参数:
            parameter: 要执行的命令
        """
        try:
            subprocess.Popen(parameter)
        except Exception as err:
            print(f"执行命令出错: {str(err)}")
