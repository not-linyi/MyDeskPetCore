import importlib
import os
from PySide6.QtGui import QIcon
from qfluentwidgets import MSFluentWindow, FluentIcon, NavigationItemPosition

from .AboutPage import AboutPage
from .PluginManage import PluginManagePage
from .Settings import SettingsPage
from src.ConfigManager import ConfigManager


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

        # 插件页面字典，用于存储已加载的插件页面
        self.plugin_pages = {}

        # 加载插件页面
        self.load_plugin_pages()

        # 创建并设置侧边栏
        self.init_navigation()

    def init_navigation(self):
        # 添加导航项
        self.addSubInterface(self.pluginManagePage,
                             FluentIcon.HOME_FILL,
                             "插件管理",
                             isTransparent=True)

        # 添加插件页面到侧边栏
        for plugin_name, page_info in self.plugin_pages.items():
            icon_name = page_info.get('icon', '')
            icon = FluentIcon.MENU if not icon_name else FluentIcon[icon_name]
            self.addSubInterface(page_info['page'],
                                 icon,
                                 page_info['chinese_name'],
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

    def switch_to_plugin_page(self, plugin_name):
        """切换到指定的插件页面
        
        Args:
            plugin_name (str): 插件名称
        """
        if plugin_name in self.plugin_pages:
            self.switchTo(self.plugin_pages[plugin_name]['page'])
            self.show()
            self.show_normal()

    def load_plugin_pages(self):
        """加载插件页面
        
        遍历所有启用的插件，检查是否有main_page字段，如果有则加载对应的页面
        """
        plugins = self.pet_parent.plugins

        for plugin_info in plugins:
            if not plugin_info.get('enabled', False):
                continue

            plugin_path = plugin_info.get('plugin_path', '')
            plugin_name = plugin_info.get('plugin_name', '')

            # 检查插件配置文件
            try:
                config_path = os.path.join(plugin_path, "config.toml")
                plugin_config = ConfigManager(config_path, create_if_not_exists=False).config

                # 检查是否有main_page字段
                if 'plugin' in plugin_config and 'main_page' in plugin_config['plugin']:
                    main_page_class = plugin_config['plugin']['main_page']
                    main_page_class_name = plugin_config['plugin']['main_page_class_name']

                    # 动态导入插件模块
                    try:
                        module_path = f"{plugin_name}.{main_page_class}"
                        module_file = os.path.join(plugin_path, f"{main_page_class}.py")

                        if os.path.exists(module_file):
                            # 创建模块规范
                            spec = importlib.util.spec_from_file_location(module_path, module_file)
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)

                            # 获取页面类并实例化
                            page_class = getattr(module, main_page_class_name)
                            page_instance = page_class(self)

                            # 存储页面信息
                            self.plugin_pages[plugin_name] = {
                                'page': page_instance,
                                'chinese_name': plugin_info.get('plugin_chinese_name', plugin_name),
                                'icon': plugin_config['plugin'].get('icon', '')
                            }
                    except Exception as e:
                        print(f"加载插件页面失败: {plugin_name}.{main_page_class}, 错误: {e}")
            except Exception as e:
                print(f"读取插件配置失败: {plugin_name}, 错误: {e}")

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
