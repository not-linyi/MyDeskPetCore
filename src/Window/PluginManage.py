from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QScrollArea, QFrame, QLabel
from qfluentwidgets import ScrollArea, SubtitleLabel, PrimaryPushButton, FluentIcon


class PluginManagePage(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("PluginManagePage")

        self.pet_parent = parent.pet_parent if hasattr(parent, 'pet_parent') else None

        self.configmanager = self.pet_parent.configmanager

        self.plugin_cards = {}

        self.vbox_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea(self)

        # 创建插件容器
        self.plugin_container = ScrollArea()
        self.plugin_container.enableTransparentBackground()
        self.plugin_layout = QVBoxLayout(self.plugin_container)

        self.setup_ui()

    def setup_ui(self):
        self.vbox_layout.setContentsMargins(20, 20, 20, 20)
        self.vbox_layout.setSpacing(10)

        # 标题和描述
        title_label = SubtitleLabel("插件管理", self)
        self.vbox_layout.addWidget(title_label)
        self.vbox_layout.addWidget(QLabel("在这里管理您的插件", self))

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

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

    def add_new_plugin(self):
        pass
