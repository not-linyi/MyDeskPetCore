from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSystemTrayIcon
from qfluentwidgets import SystemTrayMenu, Action, FluentIcon, RoundMenu

from ..Window import MainWindow


class ContextMenuEvent:
    """系统托盘菜单事件处理器

    该类用于创建并管理应用程序的系统托盘菜单，包含插件管理、关于和设置三个功能项。
    每个菜单项关联对应的页面打开方法
    """

    # 保存MainWindow实例的类变量
    main_window_instance = None

    def __init__(self, parent):
        """初始化系统托盘菜单
        
        该方法创建并配置系统托盘图标及其菜单项
        """
        # 初始化系统托盘图标组件
        self.parent = parent
        self.sysTray = QSystemTrayIcon()
        self.sysTray.setIcon(QIcon("resources/icon/logo.png"))

        # 创建插件管理器实例
        self.plugin_manager = self.parent.plugin_manager

        # 创建系统托盘菜单实例
        self.menu = SystemTrayMenu(parent=parent)

        # 配置并添加功能菜单项
        # 创建插件管理菜单项并绑定事件
        self.manageAction = Action(
            FluentIcon.HOME_FILL, "插件管理",
            triggered=lambda: self._open_manage_page()
        )
        self.menu.addAction(self.manageAction)

        # 插件菜单
        for i in self.parent.plugins:
            self.add_plugin(i)

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

    def add_plugin(self, plugin_info):
        if plugin_info['plugin_type'] != 'menu':
            return

        # 获取插件配置
        plugin_config = self.plugin_manager.get_plugin_config(plugin_info)
        if not plugin_config:
            return
            
        # 加载插件模块
        plugin = self.plugin_manager.load_plugin(plugin_info)
        if not plugin:
            return
            
        try:
            plugin_access = RoundMenu(plugin_info['plugin_chinese_name'])
            icon_name = plugin_config['plugin']['icon']
            try:
                plugin_access.setIcon(FluentIcon[icon_name])
            except KeyError:
                plugin_access.setIcon(QIcon(icon_name))

            # 尝试使用插件的自定义菜单方法
            custom_menu_created = self.plugin_manager.execute_plugin_function(plugin_info,
                                                                              'create_custom_menu',
                                                                              plugin_access)

            # 如果没有自定义菜单，则使用配置文件中的菜单项
            if not custom_menu_created and 'menu' in plugin_config:
                for menu_item in plugin_config['menu']:
                    action = Action(
                        QIcon(menu_item['menu_icon']), 
                        menu_item['menu_name'],
                        triggered=lambda _, p=menu_item['menu_parameter'], fn=menu_item["function_name"]: 
                            self.plugin_manager.execute_plugin_function(plugin_info, fn, p)
                    )
                    plugin_access.addAction(action)

            self.menu.addMenu(plugin_access)
            self.menu.addSeparator()
        except Exception as err:
            print(f"{plugin_info['plugin_name']}菜单创建出错: {str(err)}")

    def _open_manage_page(self):
        """打开插件管理页面

        """
        # 使用单例模式，如果实例不存在则创建
        if ContextMenuEvent.main_window_instance is None:
            ContextMenuEvent.main_window_instance = MainWindow.MainWindow(self.parent)
        # 显示窗口并切换到插件管理页面
        ContextMenuEvent.main_window_instance.switch_to_plugin_manage()

    def _open_about_page(self):
        """打开关于页面

        """
        # 使用单例模式，如果实例不存在则创建
        if ContextMenuEvent.main_window_instance is None:
            ContextMenuEvent.main_window_instance = MainWindow.MainWindow(self.parent)
        # 切换到关于页面并显示窗口
        ContextMenuEvent.main_window_instance.switch_to_about()

    def _open_settings_page(self):
        """打开设置页面

        """
        if ContextMenuEvent.main_window_instance is None:
            ContextMenuEvent.main_window_instance = MainWindow.MainWindow(self.parent)

        ContextMenuEvent.main_window_instance.switch_to_settings()
