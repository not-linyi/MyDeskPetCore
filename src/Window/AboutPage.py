from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
from qfluentwidgets import SubtitleLabel, CardWidget, BodyLabel, StrongBodyLabel, HyperlinkLabel, ScrollArea


# 版本信息卡片
class VersionCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.versionLayout = QVBoxLayout(self)
        self.versionTitleLabel = StrongBodyLabel("版本信息", self)
        self.versionLayout.addWidget(self.versionTitleLabel)

        self.versionInfoLabel = BodyLabel("当前版本: v0.0.4 (beta版)", self)
        self.versionLayout.addWidget(self.versionInfoLabel)

        self.architectureLabel = BodyLabel("架构特性:", self)
        self.versionLayout.addWidget(self.architectureLabel)

        self.featureLayout = QVBoxLayout()
        self.featureLayout.setContentsMargins(20, 0, 0, 0)
        features = ["插件化扩展",
                    "Live2D 渲染核心",
                    "跨平台自适应框架(?)"]
        for feature in features:
            self.featureLayout.addWidget(QLabel(f"▸ {feature}", self))

        self.versionLayout.addLayout(self.featureLayout)


# 技术卡片
class TechCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.techLayout = QVBoxLayout(self)
        self.techTitleLabel = StrongBodyLabel("技术基石", self)
        self.techLayout.addWidget(self.techTitleLabel)

        # 创建技术链接布局
        self.techLinksLayout = QHBoxLayout()
        self.techLinksLayout.setContentsMargins(0, 5, 0, 5)

        # 链接列表
        links = [
            ("PySide6", "https://www.qt.io/"),
            ("Live2D Cubism SDK", "https://www.live2d.com/"),
            ("live2d-py", "https://github.com/Arkueid/live2d-py"),
            ("qfluentWidgets", "https://qfluentwidgets.com/"),
            ("Python 3.13", "https://www.python.org/")
        ]

        # 动态生成链接并添加到布局中
        for i, (text, url) in enumerate(links):
            label = HyperlinkLabel(text, self)
            label.setUrl(url)
            self.techLinksLayout.addWidget(label)
            if i < len(links) - 1:  # 添加间距，最后一个无需间距
                self.techLinksLayout.addSpacing(20)

        # 添加弹性空间
        self.techLinksLayout.addStretch()

        # 将技术链接布局添加到主布局
        self.techLayout.addLayout(self.techLinksLayout)


# 关于团队卡片
class TeamCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.teamLayout = QVBoxLayout(self)
        self.teamTitleLabel = StrongBodyLabel("开发团队", self)
        self.teamLayout.addWidget(self.teamTitleLabel)

        self.creatorLabel = BodyLabel("创造者: 偶遇Python大作业，拼尽全力无法战胜，因为不会英语", self)
        self.teamLayout.addWidget(self.creatorLabel)

        self.thanksLabel = BodyLabel("部分代码参考:", self)
        self.teamLayout.addWidget(self.thanksLabel)

        # 添加参考列表布局
        self.referenceLayout = QVBoxLayout()
        self.referenceLayout.setContentsMargins(20, 0, 0, 0)
        # 参考项目及其链接
        references = [
            ("PyQt-Fluent-Widgets", "https://github.com/zhiyiYo/PyQt-Fluent-Widgets"),
            ("Live2D Cubism SDK for Python", "https://github.com/Arkueid/live2d-py"),
        ]

        # 使用HyperlinkLabel创建带链接的参考项
        for name, url in references:
            ref_layout = QHBoxLayout()
            ref_layout.setContentsMargins(0, 0, 0, 0)
            ref_layout.addWidget(QLabel("▸", self))
            ref_link = HyperlinkLabel(name, self)
            ref_link.setUrl(url)
            ref_layout.addWidget(ref_link)
            ref_layout.addStretch(1)
            self.referenceLayout.addLayout(ref_layout)

        self.teamLayout.addLayout(self.referenceLayout)


# 承诺卡片
class PromiseCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.promiseLayout = QVBoxLayout(self)
        self.promiseTitleLabel = StrongBodyLabel("承诺", self)
        self.promiseLayout.addWidget(self.promiseTitleLabel)

        self.promiseLayout.addWidget(BodyLabel("• 不收集个人数据", self))
        self.promiseLayout.addWidget(BodyLabel("• (不)持续维护开源核心插件", self))


# 联系方式卡片
class ContactCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.contactLayout = QVBoxLayout(self)
        self.contactTitleLabel = StrongBodyLabel("联系我们", self)
        self.contactLayout.addWidget(self.contactTitleLabel)

        self.contactLinksLayout = QHBoxLayout()
        self.contactLinksLayout.setContentsMargins(0, 5, 0, 5)

        links = [
            ("文档中心", "https://github.com/not-linyi/MyDeskPetCore/wiki"),
            ("插件工坊", "#"),
            ("GitHub", "https://github.com/not-linyi/MyDeskPetCore"),
            ("反馈通道", "kanawanaikoto@outlook.com")
        ]

        for i, (name, url) in enumerate(links):
            link = HyperlinkLabel(name, self)
            link.setUrl(url)
            self.contactLinksLayout.addWidget(link)
            if i < len(links) - 1:
                self.contactLinksLayout.addSpacing(15)

        self.contactLinksLayout.addStretch(1)
        self.contactLayout.addLayout(self.contactLinksLayout)


# 关于页面
class AboutPage(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("AboutPage")

        # 创建内容视图容器
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.setSpacing(15)

        # 设置滚动区域属性
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        # 标题部分
        self.titleLabel = SubtitleLabel("关于", self)
        self.vBoxLayout.addWidget(self.titleLabel)

        # 项目名称和描述
        self.nameLayout = QHBoxLayout()
        self.nameLayout.setContentsMargins(0, 10, 0, 10)

        # 图标
        self.iconLabel = QLabel()
        pixmap = QPixmap("resources/icon/logo.png").scaled(
            128, 128,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.iconLabel.setPixmap(pixmap)
        self.nameLayout.addWidget(self.iconLabel)
        self.nameLayout.addSpacing(15)

        # 项目名称和描述
        self.projectInfoLayout = QVBoxLayout()
        self.projectNameLabel = QLabel("My Desk Pet", self)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.projectNameLabel.setFont(font)

        self.projectDescLabel = QLabel("一个可爱的桌面宠物", self)
        self.projectInfoLayout.addWidget(self.projectNameLabel)
        self.projectInfoLayout.addWidget(self.projectDescLabel)
        self.nameLayout.addLayout(self.projectInfoLayout)
        self.nameLayout.addStretch(1)

        self.vBoxLayout.addLayout(self.nameLayout)

        # 版本信息卡片
        self.versionCard = VersionCard(self)
        self.vBoxLayout.addWidget(self.versionCard)

        # 技术基石卡片
        self.techCard = TechCard(self)
        self.vBoxLayout.addWidget(self.techCard)

        # 开发团队卡片
        self.teamCard = TeamCard(self)
        self.vBoxLayout.addWidget(self.teamCard)

        # 承诺卡片
        self.promiseCard = PromiseCard(self)
        self.vBoxLayout.addWidget(self.promiseCard)

        # 联系我们卡片
        self.contactCard = ContactCard(self)
        self.vBoxLayout.addWidget(self.contactCard)

        # 版权信息
        self.copyrightLabel = QLabel("©偶遇Python大作业，拼尽全力无法战胜，因为不会英语\n"
                                     "遵循 GPLv3 开源协议 | 保留创作最终解释权", self)
        self.copyrightLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vBoxLayout.addWidget(self.copyrightLabel)

        # 添加弹性空间
        self.vBoxLayout.addStretch(1)

        # 启用透明背景功能
        self.enableTransparentBackground()
