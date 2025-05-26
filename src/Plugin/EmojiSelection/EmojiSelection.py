from PySide6.QtGui import QIcon
from qfluentwidgets import RoundMenu, Action, FluentIcon

from src.Plugin.PluginBase import MenuPlugin


class EmojiSelectionPlugin(MenuPlugin):

    def create_custom_menu(self, params, menu):
        expression_menu = RoundMenu('表情选择')
        expression_menu.setIcon(QIcon("src/Plugin/EmojiSelection/表情.svg"))
        # 添加重置表情选项
        reset_action = Action(FluentIcon.REMOVE, '重置表情',
                              triggered=lambda: params.live2d.model.ResetExpression())
        expression_menu.addAction(reset_action)
        expression_menu.addSeparator()

        for expr in params.live2d.model.GetExpressionIds():
            action = Action(QIcon("src/Plugin/EmojiSelection/表情.svg"), expr,
                            triggered=lambda checked=False, e=expr: params.live2d.model.SetExpression(e))
            expression_menu.addAction(action)
        menu.addMenu(expression_menu)
