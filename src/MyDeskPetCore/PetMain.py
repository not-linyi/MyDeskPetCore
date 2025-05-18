import os
import sys

from PySide6.QtCore import QTimer, Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from .Live2d import Live2dModel
from .Menu import ContextMenuEvent
from ..ConfigManager import ConfigManager
from ..PluginManager import PluginManager


class PetMain(QOpenGLWidget):
    def __init__(self) -> None:
        super().__init__()

        # 配置文件路径
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.toml")
        example_config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config_example.toml")

        # 如果配置文件不存在，从示例文件复制一份
        if not os.path.exists(config_path):
            import shutil
            shutil.copyfile(example_config_path, config_path)

        # 创建配置管理器实例
        self.configmanager = ConfigManager(config_path, create_if_not_exists=False)

        # 从配置文件加载设置
        # 从配置文件中读取窗口的位置和大小设置
        self.pet_x = self.configmanager.config["window"]["x"]
        self.pet_y = self.configmanager.config["window"]["y"]
        self.window_width = self.configmanager.config["window"]["width"]
        self.window_height = self.configmanager.config["window"]["height"]
        # 从配置文件中读取缩放比例设置
        self.scale = self.configmanager.config["model"]["scale"]
        # 从配置文件中读取模型路径的设置
        self.model_path = self.configmanager.config["model"]["model_path"]
        # 从配置文件中读取动画帧率的设置
        self.frame_rate_ms = self.configmanager.config["animation"]["frame_rate_ms"]

        self.plugins = self.configmanager.config.get("plugins", [])
        # 创建插件管理器
        self.plugin_manager = PluginManager(self.plugins)
        # 执行初始化型插件
        self.plugin_manager.execute_init_plugins(self)

        # 设置初始窗口位置
        self.setGeometry(self.pet_x, self.pet_y, self.window_width, self.window_height)

        # 创建定时器用于更新模型
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 // self.frame_rate_ms)  # 1000 // (帧率) ,fps = 1000 // 60 =  16

        self.live2d = Live2dModel()

        # 创建托盘菜单
        self.tray = None

        self.draggable = False
        self.offset = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.draggable = False

    def paintGL(self):
        # 执行持续性插件
        self.plugin_manager.execute_lasting_plugins(self)

        # 更新模型状态
        self.live2d.update(self.scale)
        # 绘制模型
        self.live2d.draw()

    def initializeGL(self) -> None:
        self.live2d.initialize(self.model_path, (self.window_width, self.window_height))
        # 创建托盘菜单
        self.tray = ContextMenuEvent(self)

    # 右键菜单事件处理函数
    def contextMenuEvent(self, event):
        return self.tray.show(event.globalPos())

    def quit(self):
        # 释放Live2D资源
        self.live2d.dispose()
        # 退出应用程序
        self.close()
        sys.exit()

    def closeEvent(self, event):
        """处理窗口关闭事件
        
        确保在窗口关闭时正确释放资源，防止关闭再开时出现异常
        """

        # 清理MainWindow实例引用
        if ContextMenuEvent.main_window_instance is not None:
            ContextMenuEvent.main_window_instance = None

        # 接受关闭事件
        event.accept()
