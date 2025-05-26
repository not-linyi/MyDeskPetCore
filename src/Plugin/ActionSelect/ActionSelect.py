import json
import os

from PySide6.QtGui import QIcon
from qfluentwidgets import RoundMenu, Action

from src.Plugin.PluginBase import MenuPlugin


class ActionSelectPlugin(MenuPlugin):

    def create_custom_menu(self, params, menu):
        motion_menu = RoundMenu('动作选择')
        motion_menu.setIcon(QIcon("src/Plugin/ActionSelect/动作.svg"))

        # 添加停止所有动作选项
        stop_action = Action(QIcon("src/Plugin/ActionSelect/动作.svg"), '停止所有动作',
                             triggered=lambda: params.live2d.model.StopAllMotions())
        motion_menu.addAction(stop_action)
        motion_menu.addSeparator()

        # 获取动作组列表并添加到菜单
        motion_groups = params.live2d.model.GetMotionGroups()
        for group in motion_groups:
            # 为每个动作组创建子菜单
            group_menu = RoundMenu(group)
            group_menu.setIcon(QIcon("src/Plugin/ActionSelect/动作.svg"))

            # 添加随机动作选项
            random_action = Action(QIcon("src/Plugin/ActionSelect/动作.svg"),
                                   '随机动作',
                                   triggered=lambda checked=False,
                                   g=group: params.live2d.model.StartRandomMotion(g, 3))
            group_menu.addAction(random_action)
            group_menu.addSeparator()

            # 解析模型JSON文件，获取详细的动作信息
            motion_details = self.parse_model_json(params.model_path)

            motions = motion_details.get(group, None)

            if motions is not None:
                for i in range(motion_groups[group]):
                    action = Action(QIcon("src/Plugin/ActionSelect/动作.svg"), f'{motions[i]['name']}',
                                    triggered=lambda checked=False, g=group,
                                    idx=i: params.live2d.model.StartMotion(g, idx, 3))
                    group_menu.addAction(action)

                # 将动作组子菜单添加到主菜单
                motion_menu.addMenu(group_menu)
        menu.addMenu(motion_menu)

    @staticmethod
    def parse_model_json(model_path):
        """
        解析模型JSON文件，提取动作组和动作名称信息。
        参数:
        model_path (str): 模型JSON文件的路径。

        返回:
        dict: 包含动作组和动作名称的字典。
        """
        try:
            # 确保文件路径存在
            if not os.path.exists(model_path):
                print(f"模型文件不存在: {model_path}")
                return {}

            # 读取并解析JSON文件
            with open(model_path, 'r', encoding='utf-8') as f:
                model_data = json.load(f)

            # 提取动作信息
            motion_data = {}
            if 'FileReferences' in model_data and 'Motions' in model_data['FileReferences']:
                motions = model_data['FileReferences']['Motions']
                for group_name, motion_list in motions.items():
                    motion_data[group_name] = []
                    motion_data[group_name].extend([
                        {
                            'name': motion['Name'],
                            'file': motion.get('File', ''),
                            'sound': motion.get('Sound', None)
                        }
                        for motion in motion_list
                    ])
            return motion_data
        except Exception as e:
            print(f"解析模型JSON文件失败: {e}")
            return {}
