import os.path

import tomli
import tomli_w

# 定义泛型类型变量用于类型提示
T = TypeError('T')


class ConfigManager:
    """配置管理器类，用于处理TOML格式配置文件的加载和保存

    属性:
        config_file (str): 配置文件路径
        config (dict): 当前配置数据
        backup_config (dict): 配置数据备份
    """

    def __init__(self, config_file: str, create_if_not_exists: bool = False) -> None:
        """初始化配置管理器

        参数:
            config_file (str): 配置文件路径
            create_if_not_exists (bool): 如果配置文件不存在是否创建
        返回值:
            None
        """
        self.config_file = config_file
        self.config = {}
        self.backup_config = {}
        # 如果配置文件存在则加载，否则创建目录并初始化配置文件
        if os.path.exists(config_file):
            self.load()
        elif create_if_not_exists:
            # 创建配置文件所在目录
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            self.save()
        else:
            raise FileNotFoundError(f"配置文件 {config_file} 不存在")

    def load(self):
        """从配置文件加载配置数据到内存

        参数:
            无
        返回值:
            None
        异常:
            ValueError: TOML格式解析失败时抛出
            IOError: 文件读取失败时抛出
        """
        try:
            with open(self.config_file, "rb") as f:
                # 解析TOML格式配置文件
                self.config = tomli.load(f)
                # 创建配置备份用于异常恢复
                self.backup_config = self.config.copy()
        except tomli.TOMLDecodeError as e:
            raise ValueError(f"配置文件格式错误: {e}")
        except Exception as e:
            raise IOError(f"无法读取配置文件: {e}")

    def save(self):
        """将内存中的配置数据写入磁盘文件

        参数:
            无
        返回值:
            None
        异常:
            IOError: 文件写入失败时抛出，并自动恢复备份配置
        """
        try:
            with open(self.config_file, "wb") as f:
                # 将当前配置写入文件
                tomli_w.dump(self.config, f)
        except Exception as e:
            # 写入失败时恢复备份配置
            self.config = self.backup_config
            raise IOError(f"无法保存配置文件: {e}")
