from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QWidget, QFileDialog
from qfluentwidgets import (
    SubtitleLabel, PushButton, EditableComboBox, FluentIcon, PrimaryPushButton, IconWidget, BodyLabel,
    InfoBarIcon, TeachingTip, TeachingTipTailPosition,
    CardWidget, StrongBodyLabel, ScrollArea, ColorDialog
)


# 基类：设置卡片
class BaseSettingsCard(CardWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.titleLabel = StrongBodyLabel(title, self)
        self.vBoxLayout.addWidget(self.titleLabel)

    def addSettingItem(self, title, description, widget):
        """添加设置项"""
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)

        # 标题和描述
        info_layout = QVBoxLayout()
        title_label = QLabel(title, self)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        desc_label = QLabel(description, self)
        desc_label.setStyleSheet("font-size: 12px; color: gray;")

        info_layout.addWidget(title_label)
        info_layout.addWidget(desc_label)

        layout.addLayout(info_layout)
        layout.addStretch(1)
        layout.addWidget(widget)

        self.vBoxLayout.addLayout(layout)


# 窗口设置卡片
class WindowSettingsCard(BaseSettingsCard):
    def __init__(self, parent=None):
        super().__init__("窗口设置", parent=parent)

        # 窗口大小设置
        self.widthComboBox = EditableComboBox(self)
        self.widthComboBox.addItems(["300", "400", "500", "600"])
        self.widthComboBox.setFixedWidth(120)
        self.addSettingItem("窗口宽度", "设置桌宠窗口的宽度", self.widthComboBox)

        self.heightComboBox = EditableComboBox(self)
        self.heightComboBox.addItems(["300", "400", "500", "600"])
        self.heightComboBox.setFixedWidth(120)
        self.addSettingItem("窗口高度", "设置桌宠窗口的高度", self.heightComboBox)

        self.xComboBox = EditableComboBox(self)
        self.xComboBox.addItems(["300", "400", "500", "600", "700", "800", "900"])
        self.xComboBox.setFixedWidth(120)
        self.addSettingItem("窗口X坐标", "设置桌宠窗口出现的X坐标", self.xComboBox)

        self.yComboBox = EditableComboBox(self)
        self.yComboBox.addItems(["300", "400", "500", "600", "700", "800", "900"])
        self.yComboBox.setFixedWidth(120)
        self.addSettingItem("窗口Y坐标", "设置桌宠窗口出现的Y坐标", self.yComboBox)

        # 背景颜色设置
        self.current_bg_color = [1, 2, 3, 128]
        self.bgColorButton = PushButton("选择颜色", self)
        self.bgColorButton.setFixedWidth(120)
        self.addSettingItem("透明背景色", "设置桌宠的透明背景颜色", self.bgColorButton)


# 模型设置卡片
class ModelSettingsCard(BaseSettingsCard):
    def __init__(self, parent=None):
        super().__init__("模型设置", parent=parent)
        # 模型路径设置
        self.model_path = ""
        self.modelPathButton = PushButton("选择模型", self)
        self.modelPathButton.setFixedWidth(120)
        self.addSettingItem("模型路径", "选择Live2D模型文件", self.modelPathButton)

        # 缩放比例设置
        self.scale_combo_box = EditableComboBox(self)
        self.scale_combo_box.addItems(["0.5", "0.75", "1.0", "1.25", "1.5"])
        self.scale_combo_box.setFixedWidth(120)
        self.addSettingItem("缩放比例", "设置桌宠的缩放比例", self.scale_combo_box)


# 动画设置卡片
class AnimationSettingsCard(BaseSettingsCard):
    def __init__(self, parent=None):
        super().__init__("动画设置", parent=parent)

        # 帧率设置
        self.frameRateComboBox = EditableComboBox(self)
        self.frameRateComboBox.addItems(["30", "60", "120"])
        self.frameRateComboBox.setFixedWidth(120)
        self.addSettingItem("帧率", "设置动画的帧率(ms)", self.frameRateComboBox)


class SettingsPage(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SettingsPage")

        # 创建内容视图容器
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.setSpacing(15)

        # 设置滚动区域属性
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        # 标题部分
        self.titleLabel = SubtitleLabel("设置", self)
        self.vBoxLayout.addWidget(self.titleLabel)

        # 获取父窗口的pet_parent引用
        self.pet_parent = parent.pet_parent if hasattr(parent, 'pet_parent') else None

        # 配置管理器引用，用于保存设置
        self.configManager = self.pet_parent.configmanager

        # 创建各个设置卡片
        self.windowSettingsCard = WindowSettingsCard(self)
        self.modelSettingsCard = ModelSettingsCard(self)
        self.animationSettingsCard = AnimationSettingsCard(self)

        # 创建一个固定在底部的按钮区域
        self.bottomWidget = QWidget(self)
        self.bottomWidget.setObjectName("BottomButtonsWidget")
        self.bottomWidget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 提示图标和文本
        self.hintIcon = IconWidget(InfoBarIcon.INFORMATION, self.bottomWidget)
        self.hintLabel = BodyLabel("修改设置后点击保存生效", self.bottomWidget)

        # 保存和取消按钮
        self.saveButton = PrimaryPushButton(FluentIcon.SAVE, "保存设置", self.bottomWidget)
        self.cancelButton = PrimaryPushButton(FluentIcon.CANCEL, "还原设置", self.bottomWidget)

        # 确保窗口大小变化时底部按钮区域位置更新
        self.resizeEvent = self.onResize

        # 初始化设置界面
        self.initUI()
        self.loadSettings()

    def initUI(self):
        # 添加卡片到布局
        self.vBoxLayout.addWidget(self.windowSettingsCard)
        self.vBoxLayout.addWidget(self.modelSettingsCard)
        self.vBoxLayout.addWidget(self.animationSettingsCard)

        # 连接模型选择按钮的点击事件
        self.modelSettingsCard.modelPathButton.clicked.connect(self.selectModel)

        # 连接背景色按钮点击事件
        self.windowSettingsCard.bgColorButton.clicked.connect(self.choose_custom_color)

        # 底部按钮区域
        self.addBottomButtons()

        #  启用透明背景
        self.enableTransparentBackground()

    def addBottomButtons(self):
        bottom_layout = QHBoxLayout(self.bottomWidget)

        self.hintIcon.setFixedSize(16, 16)
        self.saveButton.clicked.connect(self.saveSettings)
        self.cancelButton.clicked.connect(self.loadSettings)

        # 底部布局
        bottom_layout.setSpacing(10)
        bottom_layout.setContentsMargins(24, 15, 24, 15)
        bottom_layout.addWidget(self.hintIcon, 0, Qt.AlignmentFlag.AlignLeft)
        bottom_layout.addWidget(self.hintLabel, 0, Qt.AlignmentFlag.AlignLeft)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.saveButton, 0, Qt.AlignmentFlag.AlignRight)
        bottom_layout.addWidget(self.cancelButton, 0, Qt.AlignmentFlag.AlignRight)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # 设置底部按钮区域固定高度
        self.bottomWidget.setFixedHeight(60)

        # 将底部按钮区域添加到父窗口而不是滚动区域
        self.setViewportMargins(0, 0, 0, 60)  # 为底部按钮区域预留空间

        # 将底部按钮区域固定在底部
        self.bottomWidget.setParent(self)
        self.bottomWidget.move(0, self.height() - 60)

    def loadSettings(self):
        """从pet_parent对象加载设置"""
        try:
            if not self.pet_parent:
                raise ValueError("无法获取桌宠对象引用")

            # 窗口设置
            width = self.pet_parent.window_width
            height = self.pet_parent.window_height
            pet_x = self.configManager.config["window"]["x"]
            pet_y = self.configManager.config["window"]["y"]

            # 设置ComboBox选项
            self.setComboBoxValue(self.windowSettingsCard.widthComboBox, str(width))
            self.setComboBoxValue(self.windowSettingsCard.heightComboBox, str(height))
            self.setComboBoxValue(self.windowSettingsCard.xComboBox, str(pet_x))
            self.setComboBoxValue(self.windowSettingsCard.yComboBox, str(pet_y))

            # 模型设置
            model_path = self.pet_parent.model_path
            self.modelSettingsCard.model_path = model_path
            scale = self.pet_parent.scale
            self.setComboBoxValue(self.modelSettingsCard.scale_combo_box, str(scale))

            # 动画设置
            frame_rate_ms = self.pet_parent.frame_rate_ms
            self.setComboBoxValue(self.animationSettingsCard.frameRateComboBox, str(frame_rate_ms))

        except Exception as e:
            self.showMessage(self.saveButton, InfoBarIcon.ERROR, "加载失败", f"加载设置失败: {str(e)}")

    def saveSettings(self):
        """保存设置到pet_parent对象并同步到配置文件"""
        try:
            if not self.pet_parent:
                raise ValueError("无法获取桌宠对象引用")

            # 从UI获取设置值
            width = int(self.windowSettingsCard.widthComboBox.currentText())
            height = int(self.windowSettingsCard.heightComboBox.currentText())
            pet_x = int(self.windowSettingsCard.xComboBox.currentText())
            pet_y = int(self.windowSettingsCard.yComboBox.currentText())
            scale = float(self.modelSettingsCard.scale_combo_box.currentText())
            frame_rate_ms = int(self.animationSettingsCard.frameRateComboBox.currentText())
            model_path = self.modelSettingsCard.model_path
            background_color = self.windowSettingsCard.current_bg_color

            # 直接更新pet_parent对象的属性
            self.pet_parent.window_width = width
            self.pet_parent.window_height = height
            self.pet_parent.scale = scale
            self.pet_parent.frame_rate_ms = frame_rate_ms
            self.pet_parent.model_path = model_path
            self.pet_parent.background_color = background_color

            # 更新桌宠对象
            self.pet_parent.timer.setInterval(1000 // frame_rate_ms)

            # 同时更新配置文件以便下次启动时保持设置
            if self.configManager:
                # 窗口设置
                if "window" not in self.configManager.config:
                    self.configManager.config["window"] = {}
                self.configManager.config["window"]["width"] = width
                self.configManager.config["window"]["height"] = height
                self.configManager.config["window"]["x"] = pet_x
                self.configManager.config["window"]["y"] = pet_y
                self.configManager.config["window"]["background_color"] = background_color

                # 模型设置
                if "model" not in self.configManager.config:
                    self.configManager.config["model"] = {}
                self.configManager.config["model"]["model_path"] = model_path
                self.configManager.config["model"]["scale"] = scale

                # 动画设置
                if "animation" not in self.configManager.config:
                    self.configManager.config["animation"] = {}
                self.configManager.config["animation"]["frame_rate_ms"] = frame_rate_ms

                # 保存配置
                self.configManager.save()

            self.showMessage(self.saveButton, InfoBarIcon.SUCCESS, "保存成功",
                             "设置已成功保存，部分设置可能需要重启应用后生效")
        except Exception as e:
            self.showMessage(self.saveButton, InfoBarIcon.ERROR, "保存失败", f"保存设置失败: {str(e)}")

    @staticmethod
    def setComboBoxValue(combo_box, value):
        """设置ComboBox的值，如果不存在则添加"""
        index = combo_box.findText(value)
        if index >= 0:
            combo_box.setCurrentIndex(index)
        else:
            combo_box.addItem(value)
            combo_box.setCurrentIndex(combo_box.count() - 1)

    def showMessage(self, target, icon, title, content):
        """显示提示消息"""
        TeachingTip.create(
            target=target,
            icon=icon,
            title=title,
            content=content,
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=2000,
            parent=self
        )

    def onResize(self, event):
        """处理窗口大小变化事件，更新底部按钮区域位置"""
        # 调整底部按钮区域的宽度和位置
        self.bottomWidget.setFixedWidth(self.width())
        self.bottomWidget.move(0, self.height() - self.bottomWidget.height())

        # 确保原始的resizeEvent处理也被调用
        super().resizeEvent(event)

    def selectModel(self):
        """选择模型文件的功能"""
        openfile_name = QFileDialog.getOpenFileName(self, '选择模型', '', '*.model3.json')
        if openfile_name[0]:
            self.modelSettingsCard.model_path = openfile_name[0]

    def choose_custom_color(self):
        """打开颜色选择对话框，让用户选择自定义背景颜色"""
        # 获取当前背景颜色
        current_color = QColor(self.windowSettingsCard.current_bg_color[0],
                               self.windowSettingsCard.current_bg_color[1],
                               self.windowSettingsCard.current_bg_color[2],
                               self.windowSettingsCard.current_bg_color[3])

        dialog = ColorDialog(current_color, '选择背景颜色', self, False)
        dialog.setWindowTitle('选择背景颜色')
        if dialog.exec():
            # 设置新的背景颜色
            color = dialog.color
            new_color = [color.red(), color.green(), color.blue(), 0]
            self.windowSettingsCard.current_bg_color = new_color
