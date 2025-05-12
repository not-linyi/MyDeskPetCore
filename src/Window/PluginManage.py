from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QScrollArea, QFrame, QLabel, QHBoxLayout
from qfluentwidgets import ScrollArea, SubtitleLabel, PrimaryPushButton, FluentIcon, CardWidget, SwitchButton, \
    BodyLabel, PushButton


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
        title_label = SubtitleLabel(self.plugin_chinese_name, self)
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

        # 创建垂直布局和滚动区域
        self.vbox_layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea(self)

        # 插件容器初始化
        self.plugin_container = ScrollArea()
        self.plugin_container.enableTransparentBackground()
        self.plugin_layout = QVBoxLayout(self.plugin_container)
        self.setup_ui()
        self.load_plugins()

    def setup_ui(self):
        """构建页面UI布局"""
        # 布局基础设置
        self.vbox_layout.setContentsMargins(20, 20, 20, 20)
        self.vbox_layout.setSpacing(10)

        # 标题和描述文本
        title_label = SubtitleLabel("插件管理", self)
        self.vbox_layout.addWidget(title_label)
        self.vbox_layout.addWidget(QLabel("在这里管理您的插件", self))

        # 滚动区域配置
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        # 插件容器布局设置
        self.plugin_layout.setContentsMargins(0, 0, 0, 0)
        self.plugin_layout.setSpacing(16)
        self.plugin_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area.setWidget(self.plugin_container)
        self.vbox_layout.addWidget(self.scroll_area)

        # 添加新插件按钮
        add_plugin_button = PrimaryPushButton("添加新插件", self)
        add_plugin_button.setIcon(FluentIcon.ADD)
        add_plugin_button.clicked.connect(self.add_new_plugin)
        self.vbox_layout.addWidget(add_plugin_button, 0, Qt.AlignmentFlag.AlignRight)

        # 启用透明背景功能
        self.enableTransparentBackground()

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
        self.plugin_layout.addWidget(card)
        self.plugin_cards[plugin_name] = card

    def add_new_plugin(self):
        """处理添加新插件操作"""
        pass

    def on_plugin_status_changed(self, plugin_name, enabled):
        """处理插件状态变化事件

        Args:
            plugin_name (str): 插件名称
            enabled (bool): 新的状态值
        """
        pass

    def on_plugin_delete_requested(self, plugin_name):
        """处理插件删除请求事件

        Args:
            plugin_name (str): 要删除的插件名称
        """
        pass
