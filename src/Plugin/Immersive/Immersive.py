from PySide6.QtCore import Qt

from src.Plugin.PluginBase import InitPlugin


class Immersive(InitPlugin):
    @staticmethod
    def immersive(parent) -> None:
        # 设置窗口属性为无边框、始终置顶
        parent.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.SubWindow
            | Qt.WindowType.WindowStaysOnTopHint)
        parent.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
