import live2d.v3 as live2d

from live2d.utils import log

live2d.setLogEnable(False)


class Live2dModel:

    def __init__(self):
        self.model = None
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
        # 更新模型位置和缩放
        self.model.SetOffset(0, 0)
        self.model.SetScale(scale)

    def draw(self):
        self.model.Draw()

    @staticmethod
    def dispose():
        """
        释放Live2D资源。
        """
        live2d.dispose()
