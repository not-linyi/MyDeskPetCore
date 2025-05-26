from PySide6.QtGui import QIcon
from qfluentwidgets import Action, FluentIcon

from src.Plugin.PluginBase import MenuPlugin


class VisibilityTogglePlugin(MenuPlugin):
    """
    桌宠显示/隐藏控制插件
    
    提供菜单选项来控制桌宠的显示和隐藏
    """
    # 桌宠可见状态，默认为可见
    pet_visible = True
    toggle_action = None

    def create_custom_menu(self, params, menu):

        # 添加显示/隐藏切换选项
        self.toggle_action = Action(FluentIcon.VIEW if self.pet_visible else FluentIcon.HIDE,
                                    '隐藏桌宠' if self.pet_visible else '显示桌宠',
                                    triggered=lambda: self.toggle_visibility(params))

        menu.addAction(self.toggle_action)

        return True

    def toggle_visibility(self, params):
        """
        切换桌宠显示/隐藏状态
        
        参数:
            params: 插件参数，包含桌宠实例
        """
        if self.pet_visible:
            # 当前可见，需要隐藏
            params.hide()
            self.pet_visible = False
            # 更新按钮文本和图标
            self.toggle_action.setText('显示桌宠')
            self.toggle_action.setIcon(FluentIcon.HIDE)
        else:
            # 当前隐藏，需要显示
            params.show()
            # 确保窗口在前台显示
            params.raise_()
            params.activateWindow()
            self.pet_visible = True
            # 更新按钮文本和图标
            self.toggle_action.setText('隐藏桌宠')
            self.toggle_action.setIcon(FluentIcon.VIEW)
