import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QWidget
from qfluentwidgets import (
    SubtitleLabel, PushButton, LineEdit, FluentIcon, PrimaryPushButton, IconWidget, BodyLabel,
    InfoBarIcon, TeachingTip, TeachingTipTailPosition, CardWidget, StrongBodyLabel, ScrollArea
)

from src.ConfigManager import ConfigManager


# 基类：菜单项卡片
class MenuItemCard(CardWidget):
    def __init__(self, menu_data, parent=None, on_delete=None):
        super().__init__(parent=parent)
        self.menu_data = menu_data
        self.on_delete = on_delete
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.setSpacing(10)
        
        # 标题和删除按钮
        header_layout = QHBoxLayout()
        self.titleLabel = StrongBodyLabel("菜单项", self)
        self.deleteButton = PushButton(FluentIcon.DELETE, "删除", self)
        self.deleteButton.clicked.connect(self._on_delete)
        
        header_layout.addWidget(self.titleLabel)
        header_layout.addStretch(1)
        header_layout.addWidget(self.deleteButton)
        self.vBoxLayout.addLayout(header_layout)
        
        # 菜单名称
        name_layout = QHBoxLayout()
        name_label = QLabel("菜单名称:", self)
        self.nameEdit = LineEdit(self)
        self.nameEdit.setText(menu_data.get("menu_name", ""))
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.nameEdit)
        self.vBoxLayout.addLayout(name_layout)
        
        # 菜单图标
        icon_layout = QHBoxLayout()
        icon_label = QLabel("图标路径:", self)
        self.iconEdit = LineEdit(self)
        self.iconEdit.setText(menu_data.get("menu_icon", ""))
        icon_layout.addWidget(icon_label)
        icon_layout.addWidget(self.iconEdit)
        self.vBoxLayout.addLayout(icon_layout)
        
        # 菜单参数
        param_layout = QHBoxLayout()
        param_label = QLabel("命令参数:", self)
        self.paramEdit = LineEdit(self)
        self.paramEdit.setText(menu_data.get("menu_parameter", ""))
        param_layout.addWidget(param_label)
        param_layout.addWidget(self.paramEdit)
        self.vBoxLayout.addLayout(param_layout)
    
    def _on_delete(self):
        if self.on_delete:
            self.on_delete(self)
    
    def get_menu_data(self):
        return {
            "menu_name": self.nameEdit.text(),
            "menu_icon": self.iconEdit.text(),
            "menu_parameter": self.paramEdit.text(),
        }


class ConfigPage(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("QuickStartPage")
        
        # 创建内容视图容器
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.setSpacing(15)
        
        # 设置滚动区域属性
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        
        # 标题部分
        self.titleLabel = SubtitleLabel("快速命令配置", self)
        self.vBoxLayout.addWidget(self.titleLabel)

        # 获取插件路径
        self.plugin_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.plugin_path, "config.toml")

        # 菜单项容器
        self.menu_container = QWidget(self)
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.vBoxLayout.addWidget(self.menu_container)
        self.vBoxLayout.addStretch()  # 添加拉伸因子

        # 添加按钮
        self.addButton = PrimaryPushButton(FluentIcon.ADD, "添加菜单项", self)
        self.addButton.clicked.connect(self.add_menu_item)
        self.vBoxLayout.addWidget(self.addButton)
        
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
        # 底部按钮区域
        self.addBottomButtons()

        #  启用透明背景
        self.enableTransparentBackground()
        
        # 连接按钮事件
        self.saveButton.clicked.connect(self.saveSettings)
        self.cancelButton.clicked.connect(self.loadSettings)
    
    def addBottomButtons(self):
        bottom_layout = QHBoxLayout(self.bottomWidget)
        
        self.hintIcon.setFixedSize(16, 16)
        
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
    
    def onResize(self, event):
        """处理窗口大小变化事件，更新底部按钮区域位置"""
        # 调整底部按钮区域的宽度和位置
        self.bottomWidget.setFixedWidth(self.width())
        self.bottomWidget.move(0, self.height() - self.bottomWidget.height())
        
        # 确保原始的resizeEvent处理也被调用
        super().resizeEvent(event)
    
    def loadSettings(self):
        """从配置文件加载设置"""
        try:
            # 清空现有菜单项
            self.clear_menu_items()
            
            # 读取配置文件
            if os.path.exists(self.config_path):
                config_manager = ConfigManager(self.config_path)
                menu_items = config_manager.config.get("menu", [])
                
                # 添加菜单项卡片
                for menu_item in menu_items:
                    self.add_menu_item(menu_item)
            
        except Exception as e:
            self.showMessage(self.saveButton, InfoBarIcon.ERROR, "加载失败", f"加载设置失败: {str(e)}")
    
    def clear_menu_items(self):
        """清空所有菜单项"""
        # 清空布局中的所有控件
        while self.menu_layout.count():
            item = self.menu_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def add_menu_item(self, menu_data=None):
        """添加菜单项卡片"""
        if menu_data is False:
            menu_data = {
                "menu_name": "",
                "menu_icon": "",
                "menu_parameter": "",
                "function_name": "execute_command"
            }
        
        menu_card = MenuItemCard(menu_data, self, on_delete=self.delete_menu_item)
        self.menu_layout.addWidget(menu_card)
    
    def delete_menu_item(self, card):
        """删除菜单项卡片"""
        self.menu_layout.removeWidget(card)
        card.deleteLater()
    
    def saveSettings(self):
        """保存设置到配置文件"""
        try:
            if not os.path.exists(self.config_path):
                return
            config_manager = ConfigManager(self.config_path)
            config = config_manager.config
            
            # 收集所有菜单项数据
            menu_items = []
            for i in range(self.menu_layout.count()):
                item = self.menu_layout.itemAt(i)
                if item and item.widget():
                    card = item.widget()
                    if isinstance(card, MenuItemCard):
                        menu_data = card.get_menu_data()
                        # 验证必填字段
                        if menu_data["menu_name"] and menu_data["menu_parameter"]:
                            menu_data["function_name"] = "execute_command"
                            menu_items.append(menu_data)
            
            # 更新配置
            config["menu"] = menu_items
            
            # 保存配置
            config_manager.save()
            
            self.showMessage(self.saveButton, InfoBarIcon.SUCCESS, "保存成功", "设置已成功保存")
        except Exception as e:
            self.showMessage(self.saveButton, InfoBarIcon.ERROR, "保存失败", f"保存设置失败: {str(e)}")
    
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
