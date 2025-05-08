from PySide6.QtCore import QTimer
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from .Live2d import Live2dModel


class PetMain(QOpenGLWidget):
    def __init__(self) -> None:
        super().__init__()

        # 创建Live2D模型实例
        self.window_width = 400
        self.window_height = 400
        self.model_path = "resources/Live2dModel/Firefly-desktop/Firefly.model3.json"
        self.live2d = Live2dModel()

        # 创建定时器用于更新模型
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 // 60)  # 1000 // (帧率) ,fps = 1000 // 60 =  16


    def paintGL(self):
        # 更新模型状态
        self.live2d.update(0.8)
        # 绘制模型
        self.live2d.draw()
    def initializeGL(self) -> None:
        self.live2d.initialize(self.model_path, (self.window_width, self.window_height))
