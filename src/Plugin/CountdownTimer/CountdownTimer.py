import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSpinBox, QDialog, QDialogButtonBox, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QIcon
from qfluentwidgets import PrimaryToolButton, FluentIcon

from src.Plugin.PluginBase import MenuPlugin


class CircularProgressBar(QWidget):
    def __init__(self, waittime):
        super().__init__()
        self.waittime = waittime
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        # 设置窗口黑色背景
        self.setStyleSheet("background-color: black;")

        self.setWindowTitle("倒计时")
        self.setWindowIcon(QIcon("resources/icon/logo.png"))

        self.setGeometry(100, 100, 360, 360)

        self.progress = self.waittime  # 初始进度设置为满（100%）
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)

        self.remaining_time = self.waittime  # 将等待时间设置为初始值
        self.remaining_label = QLabel(self)
        self.remaining_label.setFont(QFont("Arial", 36))  # 调整字体大小以适应时:分:秒格式
        self.remaining_label.setStyleSheet("color: white;")  # 白色字体
        self.remaining_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.remaining_label.setGeometry(60, 140, 240, 80)  # 调整标签位置和大小

        self.is_running = False  # 标记进度条是否正在运行

        # 创建按钮
        self.createButtons()

        # 启动定时器
        self.startProgress()

    def updateProgress(self):
        self.progress -= 1
        if self.progress < 0:
            self.progress = 0
        self.remaining_time -= 1
        if self.remaining_time < 0:
            self.remaining_time = 0
            self.timer.stop()
            self.is_running = False
            # 倒计时结束时播放系统提示音
            QApplication.beep()
            # 倒计时结束时显示提醒对话框
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("倒计时结束")
            msg_box.setText("您设置的倒计时已结束！")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setStyleSheet("QLabel{color: white;} QPushButton{color: white; background-color: #346ee7;}")
            msg_box.exec()
            self.hide()
            self.deleteLater()

        hours = self.remaining_time // 3600
        minutes = (self.remaining_time % 3600) // 60
        seconds = self.remaining_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.remaining_label.setText(time_str)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        rect.adjust(20, 20, -20, -20)
        center = rect.center()

        # 画背景圆
        painter.setPen(QPen(QColor(60, 60, 60), 20))  # 深灰色背景圆，与黑色背景有对比
        painter.drawEllipse(rect)

        # 画进度圆（带弧度）
        angle = int(360 * (self.progress / self.waittime))  # 将angle转换为整数，现在是从满到空

        # 创建带有圆角的QPen
        pen = QPen(QColor(52, 110, 231), 20)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)  # 设置Pen的Cap Style为圆角

        painter.setPen(pen)

        # 计算圆弧的起始角度和角度范围
        start_angle = 90 * 16  # 从12点钟方向开始
        span_angle = -angle * 16  # 负角度表示逆时针方向

        painter.drawArc(rect, start_angle, span_angle)

    def createButtons(self):
        # 创建按钮容器
        button_container = QWidget(self)
        button_layout = QHBoxLayout(button_container)

        # 创建暂停/继续按钮
        self.pause_button = PrimaryToolButton(FluentIcon.PLAY)
        self.pause_button.clicked.connect(self.togglePause)

        # 创建结束按钮
        self.end_button = PrimaryToolButton(FluentIcon.POWER_BUTTON)
        self.end_button.clicked.connect(self.endProgress)

        # 添加按钮到布局
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.end_button)

        # 设置按钮容器的位置和大小
        button_container.setGeometry(80, 240, 200, 40)

    def startProgress(self):
        if not self.is_running:
            self.timer.start(1000)
            self.is_running = True
            self.pause_button.setIcon(FluentIcon.PAUSE)

    def togglePause(self):
        if self.is_running:
            # 暂停计时器
            self.timer.stop()
            self.is_running = False
            self.pause_button.setIcon(FluentIcon.PLAY)
        else:
            # 继续计时器
            self.timer.start(1000)
            self.is_running = True
            self.pause_button.setIcon(FluentIcon.PAUSE)

    def endProgress(self):
        # 只关闭当前窗口，不影响主应用程序
        self.hide()
        self.deleteLater()  # 安全释放窗口资源
        
    def closeEvent(self, event):
        # 重写关闭事件，防止关闭窗口时退出整个应用
        event.accept()  # 接受关闭事件但不退出应用
        self.hide()  # 隐藏窗口
        self.deleteLater()  # 安全释放窗口资源


class TimeInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置倒计时时间")
        self.resize(300, 150)

        # 创建布局
        layout = QVBoxLayout(self)

        # 创建时分秒输入框
        time_layout = QHBoxLayout()

        # 小时输入框
        self.hour_spinbox = QSpinBox(self)
        self.hour_spinbox.setRange(0, 23)
        self.hour_spinbox.setSuffix(" 时")

        # 分钟输入框
        self.minute_spinbox = QSpinBox(self)
        self.minute_spinbox.setRange(0, 59)
        self.minute_spinbox.setSuffix(" 分")

        # 秒输入框
        self.second_spinbox = QSpinBox(self)
        self.second_spinbox.setRange(0, 59)
        self.second_spinbox.setSuffix(" 秒")

        # 添加到布局
        time_layout.addWidget(self.hour_spinbox)
        time_layout.addWidget(self.minute_spinbox)
        time_layout.addWidget(self.second_spinbox)

        # 创建按钮
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # 添加到主布局
        layout.addLayout(time_layout)
        layout.addWidget(button_box)

    def get_seconds(self):
        """获取设置的总秒数"""
        hours = self.hour_spinbox.value()
        minutes = self.minute_spinbox.value()
        seconds = self.second_spinbox.value()

        return hours * 3600 + minutes * 60 + seconds


class CountdownTimerPlugin(MenuPlugin):
    """倒计时插件
    
    在系统托盘菜单中添加倒计时选项，可以设置不同的倒计时时间
    """
    
    def initialize(self) -> bool:
        """初始化插件
        
        返回值:
            bool: 初始化是否成功
        """
        return True

    def start_countdown(self, seconds):
        """启动倒计时

        参数:
            seconds: 倒计时秒数
        """
        try:
            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)

            window = CircularProgressBar(waittime=int(seconds))
            window.show()
            
            # 保持窗口引用，防止被垃圾回收
            self.countdown_window = window

        except Exception as err:
            print(f"启动倒计时出错: {str(err)}")
            import traceback
            traceback.print_exc()

    def custom_countdown(self, _):
        """自定义倒计时时间
        
        参数:
            _: 占位参数，不使用
        """
        try:
            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)

            dialog = TimeInputDialog()
            
            # 保持对话框引用
            self.dialog = dialog
            
            if dialog.exec():
                seconds = dialog.get_seconds()
                if seconds > 0:
                    self.start_countdown(seconds)
        except Exception as err:
            print(f"自定义倒计时出错: {str(err)}")
            import traceback
            traceback.print_exc()