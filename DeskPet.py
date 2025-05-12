import sys

from PySide6.QtWidgets import QApplication

from src.MyDeskPetCore.PetMain import PetMain

if __name__ == "__main__":
    # 创建QApplication实例，传递命令行参数
    app = QApplication(sys.argv)
    # 创建PetMain实例(主窗口的实例)
    pet_main = PetMain()
    # 显示主窗口
    pet_main.show()
    # 运行应用程序，进入事件循环
    app.exec()
    # 退出程序，返回0表示正常退出
    sys.exit(0)
