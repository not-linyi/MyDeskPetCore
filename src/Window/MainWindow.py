from PySide6.QtGui import QIcon
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition

from .AboutPage import AboutPage
from .PluginManage import PluginManagePage


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
        self.navigationInterface.setCurrentItem(self.pluginManagePage.objectName())

    def switch_to_about(self):
        """切换到关于页面"""
        self.switchTo(self.aboutPage)
        self.show()
        if self.isMinimized():
            self.showNormal()

    def switch_to_plugin_manage(self):
        """切换到插件管理页面"""
        self.switchTo(self.pluginManagePage)
        self.show()
        self.show_normal()
        if self.isMinimized():
            self.showNormal()

    def show_normal(self):
        """恢复窗口显示
        
        针对不同环境（特别是KDE6/Wayland）进行了优化处理，
        确保窗口能够从最小化状态正确恢复并获得焦点
        """
        # 如果窗口被最小化，则恢复正常显示
        if self.isMinimized():
            self.showNormal()

        # 提升窗口层级
        self.raise_()

        self.activateWindow()

    def closeEvent(self, event):
        """处理窗口关闭事件

        重写closeEvent方法，确保窗口关闭时正确清理资源，
        防止关闭再开时出现异常
        """
        # 从Menu.py的ContextMenuEvent类中清除MainWindow实例引用
        from ..MyDeskPetCore.Menu import ContextMenuEvent
        ContextMenuEvent.main_window_instance = None

        # 接受关闭事件，允许窗口关闭
        event.accept()
