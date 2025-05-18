from PySide6.QtGui import QIcon
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition

from .AboutPage import AboutPage
from .PluginManage import PluginManagePage
from .Settings import SettingsPage


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
        self.pluginManagePage = PluginManagePage(self)
        self.aboutPage = AboutPage(self)
        self.settingsPage = SettingsPage(self)

        # 创建并设置侧边栏
        self.init_navigation()

    def init_navigation(self):
        # 添加导航项
        self.addSubInterface(self.pluginManagePage,
                             FluentIcon.HOME_FILL,
                             "插件管理",
                             isTransparent=True)
        self.addSubInterface(self.aboutPage,
                             FluentIcon.INFO,
                             "关于",
                             position=NavigationItemPosition.BOTTOM,
                             isTransparent=True)
        self.addSubInterface(self.settingsPage,
                             FluentIcon.SETTING,
                             "设置",
                             position=NavigationItemPosition.BOTTOM,
                             isTransparent=True)

        self.navigationInterface.setCurrentItem(self.pluginManagePage.objectName())

    def switch_to_about(self):
        """切换到关于页面"""
        self.switchTo(self.aboutPage)
        self.show()
        self.show_normal()

    def switch_to_plugin_manage(self):
        """切换到插件管理页面"""
        self.switchTo(self.pluginManagePage)
        self.show()
        self.show_normal()

    def switch_to_settings(self):
        """切换到设置页面"""
        self.switchTo(self.settingsPage)
        self.show()
        self.show_normal()

    def show_normal(self):
        """恢复窗口显示

        确保窗口能够从最小化状态正确恢复并获得焦点
        """
        # 如果窗口被最小化，则恢复正常显示
        if self.isMinimized():
            self.showNormal()

        # 提升窗口层级
        self.raise_()

        self.activateWindow()

    def closeEvent(self, event):
        # 重写关闭事件，使窗口关闭时只隐藏而不销毁
        # 这样可以防止关闭此窗口时影响Pet窗口
        event.ignore()
        self.hide()
