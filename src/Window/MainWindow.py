from PySide6.QtGui import QIcon
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition

from .AboutPage import AboutPage


class MainWindow(MSFluentWindow):
    def __init__(self, pet_parent):
        super().__init__()
        self.pet_parent = pet_parent

        # 设置窗口标题和大小
        self.setWindowTitle("桌宠管理")
        self.setWindowIcon(QIcon("resources/icon/logo.png"))
        self.resize(900, 650)

        self.setMinimumSize(900, 650)

        # 创建页面
        self.aboutPage = AboutPage(self)

        # 创建并设置侧边栏
        self.init_navigation()

    def init_navigation(self):
        # 添加导航项
        self.addSubInterface(self.aboutPage,
                             FluentIcon.INFO,
                             "关于",
                             position=NavigationItemPosition.BOTTOM,
                             isTransparent=True)

    def switch_to_about(self):
        """切换到关于页面"""
        self.switchTo(self.aboutPage)
        self.show()


