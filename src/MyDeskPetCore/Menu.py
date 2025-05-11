from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSystemTrayIcon

from qfluentwidgets import SystemTrayMenu, Action, FluentIcon

from ..Window import MainWindow


class ContextMenuEvent:
    """系统托盘菜单事件处理器

    该类用于创建并管理应用程序的系统托盘菜单，包含插件管理、关于和设置三个功能项。
    每个菜单项关联对应的页面打开方法，当前方法体暂未实现。
    """

    # 保存MainWindow实例的类变量
    _main_window_instance = None

    def __init__(self, parent):
        """初始化系统托盘菜单

        """
        # 初始化系统托盘图标组件
        self.parent = parent
        self.sysTray = QSystemTrayIcon()
        self.sysTray.setIcon(QIcon("resources/icon/logo.png"))

        # 创建系统托盘菜单实例
        self.menu = SystemTrayMenu(parent=parent)

        # 配置并添加功能菜单项
        # 创建插件管理菜单项并绑定事件
        self.manageAction = Action(
            FluentIcon.HOME_FILL, "插件管理",
            triggered=lambda: self._open_manage_page()
        )
        self.menu.addAction(self.manageAction)

        # 创建关于菜单项并绑定事件
        self.about_action = Action(FluentIcon.INFO, '关于',
                                   triggered=lambda: self._open_about_page())
        self.menu.addAction(self.about_action)

        # 创建设置菜单项并绑定事件
        self.settings_action = Action(FluentIcon.SETTING, '设置',
                                      triggered=lambda: self._open_settings_page())
        self.menu.addAction(self.settings_action)

        # 添加退出菜单项
        self.exit_action = Action(FluentIcon.EMBED, '退出', triggered=lambda: self.parent.quit())
        self.menu.addAction(self.exit_action)

        # 将菜单绑定到系统托盘
        self.sysTray.setContextMenu(self.menu)
        self.sysTray.show()

    def show(self, pos):
        # 显示右键菜单
        self.menu.exec(pos)

    def _open_manage_page(self):
        """打开插件管理页面

        当前为空实现，需后续扩展具体页面打开逻辑
        """
        pass

    def _open_about_page(self):
        """打开关于页面

        当前为空实现，需后续扩展具体页面打开逻辑
        """
        # 使用单例模式，如果实例不存在则创建
        if ContextMenuEvent._main_window_instance is None:
            ContextMenuEvent._main_window_instance = MainWindow.MainWindow(self.parent)
        # 切换到关于页面并显示窗口
        ContextMenuEvent._main_window_instance.switch_to_about()

    def _open_settings_page(self):
        """打开设置页面

        当前为空实现，需后续扩展具体页面打开逻辑
        """
        pass
