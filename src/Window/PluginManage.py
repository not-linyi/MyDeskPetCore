import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QWidget
from qfluentwidgets import ScrollArea, SubtitleLabel, PrimaryPushButton, FluentIcon, CardWidget, SwitchButton, \
    BodyLabel, PushButton, InfoBar, InfoBarPosition, StrongBodyLabel

from src.ConfigManager import ConfigManager


class PluginCard(CardWidget):
    """插件卡片组件，用于展示单个插件的详细信息及操作控件

    Attributes:
        statusChanged (Signal): 插件状态变化信号，参数(plugin_name: str, enabled: bool)
        deleteRequested (Signal): 删除插件请求信号，参数(plugin_name: str)
    """
    statusChanged = Signal(str, bool)  # 插件状态变化信号
    deleteRequested = Signal(str)  # 删除插件请求信号

    def __init__(self, plugin_info):
        """初始化插件卡片

        Args:
            plugin_info (dict): 插件信息字典，包含以下字段：
                plugin_path (str): 插件文件路径
                plugin_name (str): 插件英文名称
                plugin_chinese_name (str): 插件中文名称
                type (str): 插件类型
                enabled (bool): 是否启用状态
        """
        super().__init__()
        self.plugin_info = plugin_info
        self.plugin_path = plugin_info.get('plugin_path', '')
        self.plugin_name = plugin_info.get('plugin_name', '')
        self.plugin_chinese_name = plugin_info.get('plugin_chinese_name', '')
        self.plugin_type = plugin_info.get('plugin_type', '')
        self.enabled = plugin_info.get('enabled', False)
        self.setup_ui()

    def setup_ui(self):
        """构建UI界面布局"""
        # 主布局设置
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)

        # 标题行布局（包含中文名称和开关按钮）
        title_layout = QHBoxLayout()
        title_label = StrongBodyLabel(self.plugin_chinese_name, self)
        title_layout.addWidget(title_label)
        title_layout.addStretch(1)

        # 状态切换开关
        switch = SwitchButton(self)
        switch.setChecked(self.enabled)
        switch.checkedChanged.connect(self._on_status_changed)
        title_layout.addWidget(switch)
        main_layout.addLayout(title_layout)

        # 插件信息展示区域
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        # 路径信息展示
        path_layout = QHBoxLayout()
        path_label = BodyLabel("路径: ", self)
        path_value = BodyLabel(self.plugin_path, self)
        path_layout.addWidget(path_label)
        path_layout.addWidget(path_value)
        path_layout.addStretch()
        info_layout.addLayout(path_layout)

        # 英文名称展示
        name_layout = QHBoxLayout()
        name_label = BodyLabel("名称: ", self)
        name_value = BodyLabel(self.plugin_name, self)
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_value)
        name_layout.addStretch()
        info_layout.addLayout(name_layout)

        # 插件类型展示
        type_layout = QHBoxLayout()
        type_label = BodyLabel("类型: ", self)
        type_value = BodyLabel(self.plugin_type, self)
        type_layout.addWidget(type_label)
        type_layout.addWidget(type_value)
        type_layout.addStretch()
        info_layout.addLayout(type_layout)

        main_layout.addLayout(info_layout)

        # 操作按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        # 删除按钮
        delete_button = PushButton("删除", self)
        delete_button.setIcon(FluentIcon.DELETE)
        delete_button.clicked.connect(self._on_delete_clicked)
        button_layout.addWidget(delete_button)
        main_layout.addLayout(button_layout)

    def _on_status_changed(self, checked):
        """处理状态开关变化事件

        Args:
            checked (bool): 新的启用状态
        """
        self.enabled = checked
        self.statusChanged.emit(self.plugin_name, checked)

    def _on_delete_clicked(self):
        """处理删除按钮点击事件"""
        self.deleteRequested.emit(self.plugin_name)


class PluginManagePage(ScrollArea):
    """插件管理页面，提供插件列表展示和管理功能"""

    def __init__(self, parent=None):
        """初始化管理页面

        Args:
            parent (QWidget): 父级窗口部件
        """
        super().__init__(parent=parent)
        self.setObjectName("PluginManagePage")

        self.pet_parent = parent.pet_parent if hasattr(parent, 'pet_parent') else None
        self.configmanager = self.pet_parent.configmanager
        self.plugin_cards = {}

        # 创建内容视图容器
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.setSpacing(15)

        # 描述文本
        self.descLabel = BodyLabel("在这里管理您的插件", self)

        # 标题部分
        self.titleLabel = SubtitleLabel("插件管理", self)

        # 底部按钮区域
        self.bottomLayout = QHBoxLayout()
        # 添加新插件按钮
        self.addPluginButton = PrimaryPushButton("添加新插件", self)

        # 插件容器区域
        self.pluginsContainer = QWidget(self)
        self.pluginsLayout = QVBoxLayout(self.pluginsContainer)

        # 设置滚动区域属性
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.setup_ui()
        self.load_plugins()

        # 启用透明背景功能
        self.enableTransparentBackground()

    def setup_ui(self):
        """构建页面UI布局"""
        self.vBoxLayout.addWidget(self.titleLabel)

        self.vBoxLayout.addWidget(self.descLabel)

        self.pluginsLayout.setContentsMargins(0, 10, 0, 10)
        self.pluginsLayout.setSpacing(15)
        self.pluginsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 添加插件容器到主布局
        self.vBoxLayout.addWidget(self.pluginsContainer)

        # 添加弹性空间
        self.vBoxLayout.addStretch(1)

        self.bottomLayout.setContentsMargins(0, 10, 0, 0)

        self.addPluginButton.setIcon(FluentIcon.ADD)
        self.addPluginButton.clicked.connect(self.add_new_plugin)

        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.addPluginButton)

        # 添加底部布局到主布局
        self.vBoxLayout.addLayout(self.bottomLayout)

    def load_plugins(self):
        """加载配置中的插件信息并生成卡片"""
        self.configmanager.load()

        # 获取插件列表
        plugins = self.pet_parent.plugins

        # 创建插件卡片
        for plugin_info in plugins:
            self.add_plugin_card(plugin_info)

    def add_plugin_card(self, plugin_info):
        """添加插件卡片到界面

        Args:
            plugin_info (dict): 插件信息字典
        """
        plugin_name = plugin_info.get('plugin_name', '')
        if not plugin_name:
            return

        # 创建插件卡片
        card = PluginCard(plugin_info)
        card.statusChanged.connect(self.on_plugin_status_changed)
        card.deleteRequested.connect(self.on_plugin_delete_requested)

        # 添加到布局
        self.pluginsLayout.addWidget(card)
        self.plugin_cards[plugin_name] = card

    def add_new_plugin(self):
        """处理添加新插件操作"""
        config_path = ""
        # 选择插件目录
        plugin_dir = QFileDialog.getExistingDirectory(
            self, "选择插件目录",
            os.path.join(os.path.dirname(config_path), "src", "plugin")
        )

        if not plugin_dir:
            return

        # 检查是否是有效插件目录
        config_file = os.path.join(plugin_dir, "config.toml")
        if not os.path.exists(config_file):
            QMessageBox.warning(
                self, "无效的插件",
                f"所选目录不是有效的插件目录，缺少必要的文件:\n"
                f"- config.toml\n"
            )
            return
        new_plugin = None
        try:
            plugin_config_manager = ConfigManager(config_file, create_if_not_exists=False)
            plugin_name = plugin_config_manager.config.get('plugin').get('plugin_name')

            new_plugin = plugin_config_manager.config.get('plugin')
            new_plugin['plugin_path'] = plugin_dir
            new_plugin['enabled'] = True

            # 更新配置
            if 'plugins' not in self.configmanager.config:
                self.configmanager.config['plugins'] = []

            # 检查是否已存在
            for existing_plugin in self.configmanager.config['plugins']:
                if existing_plugin.get('plugin_name') == plugin_name:
                    QMessageBox.warning(
                        self, "插件已存在",
                        f"插件 '{plugin_name}' 已经存在，不能重复添加。"
                    )
                    return
        except Exception as e:
            QMessageBox.warning(
                self, "无效的插件",
                f"所选目录不是有效的插件目录，无法读取配置文件:\n"
                f"- {config_file}\n"
                f"错误信息:\n"
                f"{e}"
            )
            return

        try:
            # 添加新插件
            self.configmanager.config['plugins'].append(new_plugin)
            # 保存配置
            self.configmanager.save()
            self.pet_parent.plugins = self.configmanager.config['plugins']
            # 添加插件卡片
            self.add_plugin_card(new_plugin)
            # 显示成功消息
            InfoBar.success(
                title="添加成功",
                content=f"插件 '{new_plugin['plugin_chinese_name'] or new_plugin['plugin_name']}' 已成功添加",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        except Exception as e:
            QMessageBox.critical(
                self, "保存失败",
                f"保存配置文件时出错: {str(e)}"
            )

    def on_plugin_status_changed(self, plugin_name, enabled):
        """处理插件状态变化事件

        Args:
            plugin_name (str): 插件名称
            enabled (bool): 新的状态值
        """
        status = "启用" if enabled else "禁用"
        InfoBar.info(
            title=f"插件{status}",
            content=f"插件 '{plugin_name}' 已{status}",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=2000,
            parent=self
        )

        for plugin in self.configmanager.config['plugins']:
            if plugin['plugin_name'] == plugin_name:
                plugin['enabled'] = enabled
                break
        try:
            self.configmanager.save()
            self.pet_parent.plugins = self.configmanager.config['plugins']
        except Exception as e:
            QMessageBox.critical(
                self, "保存失败",
                f"保存配置文件时出错: {str(e)}"
            )

    def on_plugin_delete_requested(self, plugin_name):
        """处理插件删除请求事件

        Args:
            plugin_name (str): 要删除的插件名称
        """
        # 确认删除
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除插件 '{plugin_name}' 吗？\n\n注意：这只会从配置中移除插件，不会删除插件文件。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            # 从配置中移除插件
            plugins = self.configmanager.config.get('plugins', [])
            for i, plugin in enumerate(plugins):
                if plugin.get('plugin_name') == plugin_name:
                    del plugins[i]
                    break
            self.pet_parent.plugins = plugins
            # 保存配置
            self.configmanager.save()
            # 移除插件卡片
            if plugin_name in self.plugin_cards:
                self.plugin_cards[plugin_name].setParent(None)
                del self.plugin_cards[plugin_name]
            # 显示成功消息
            InfoBar.success(
                title="删除成功",
                content=f"插件 '{plugin_name}' 已成功删除",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        except Exception as e:
            QMessageBox.critical(
                self, "删除失败",
                f"删除时出错: {str(e)}"
            )
