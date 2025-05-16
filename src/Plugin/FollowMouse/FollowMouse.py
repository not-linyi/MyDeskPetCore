import pyautogui
from src.Plugin.PluginBase import LastingPlugin


class FollowMousePlugin(LastingPlugin):
    """鼠标跟随插件
    
    在每一帧更新时执行，使宠物跟随鼠标移动
    """
    
    def update(self, parent) -> None:
        """更新方法，在每一帧调用
        
        参数:
            parent: 父对象，通常是PetMain实例
        """
        # 全屏跟随：获取屏幕上的鼠标位置
        screen_x, screen_y = pyautogui.position()
        # 转换为窗口相对坐标
        x = screen_x - parent.pet_x
        y = screen_y - parent.pet_y
        parent.live2d.model.Drag(x, y)
