from src.Plugin.PluginBase import InitPlugin


class ImmersivePlus(InitPlugin):
    @staticmethod
    def immersive_plus(parent) -> None:
        try:
            hwnd = int(parent.winId())
            background_color = parent.background_color
            import win32gui
            import win32con
            import win32api
            # 启用层叠窗口扩展样式
            exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exstyle | win32con.WS_EX_LAYERED)
            # 设置颜色键
            win32gui.SetLayeredWindowAttributes(hwnd,
                                                win32api.RGB(background_color[0],
                                                             background_color[1],
                                                             background_color[2]),
                                                0, win32con.LWA_COLORKEY)
            # 将窗口置顶并保持位置与大小
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            # 移除标题栏和边框样式
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            style &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
            win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
            exstyle &= ~win32con.WS_EX_TRANSPARENT
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exstyle)
        except Exception as e:
            print(f"设置窗口属性失败: {e}")
