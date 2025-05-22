import live2d.v3 as live2d

from live2d.utils import log
from live2d.utils.lipsync import WavHandler
from live2d.v3 import StandardParams

live2d.setLogEnable(False)


class Live2dModel:

    def __init__(self):
        self.model = None
        # 唇形同步相关
        self.wavHandler = WavHandler()
        self.lipSyncN = 2.5
        live2d.init()

    def initialize(self, model_path, display_size):
        try:
            if live2d.LIVE2D_VERSION == 3:
                live2d.glInit()
                self.model = live2d.LAppModel()
                self.model.LoadModelJson(model_path)
                # 设置模型大小
                self.model.Resize(*display_size)
            else:
                log.Error("不支持的live2d模型")

        except Exception as e:
            log.Error(f"初始化模型失败: {e}")
            return False

    def update(self, scale):
        self.model.Update()

        # 更新唇形同步
        if self.wavHandler.Update():
            self.model.AddParameterValue(
                StandardParams.ParamMouthOpenY, self.wavHandler.GetRms() * self.lipSyncN
            )

        # 更新模型位置和缩放
        self.model.SetOffset(0, 0)
        self.model.SetScale(scale)

    def draw(self, background_color):
        # 清除缓冲区并绘制模型，避免残影
        live2d.clearBuffer(background_color[0] / 255,
                           background_color[1] / 255,
                           background_color[2] / 255,
                           0)
        self.model.Draw()

    @staticmethod
    def dispose():
        """
        释放Live2D资源。
        """
        live2d.dispose()
