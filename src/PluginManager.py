import importlib.util
import inspect
import os
from typing import Any, Dict, List, Optional

from .ConfigManager import ConfigManager
from src.Plugin.PluginBase import PluginBase, MenuPlugin, LastingPlugin, InitPlugin


class PluginManager:
    """插件管理器类
    
    用于统一管理插件的加载、初始化和执行，避免重复加载模块
    
    属性:
        plugins (list): 插件配置列表
        loaded_plugins (dict): 已加载的插件模块
        plugin_instances (dict): 已实例化的插件对象
        plugin_types (dict): 插件类型缓存，用于避免重复的类型检查
    """
    
    def __init__(self, plugins: List[Dict[str, Any]]):
        """初始化插件管理器
        
        参数:
            plugins (List[Dict[str, Any]]): 插件配置列表
        """
        self.plugins = plugins
        # 缓存已加载的插件模块
        self.loaded_plugins = {}
        # 缓存已实例化的插件对象
        self.plugin_instances = {}
        # 缓存插件类型，避免重复的类型检查
        self.plugin_types = {}
        
    def load_plugin(self, plugin_info: Dict[str, Any]) -> Optional[Any]:
        """加载插件模块
        
        参数:
            plugin_info (Dict[str, Any]): 插件信息
            
        返回值:
            Optional[Any]: 加载的插件模块，加载失败则返回None
        """
        plugin_name = plugin_info['plugin_name']
        
        # 如果插件已经加载，直接返回
        if plugin_name in self.loaded_plugins:
            return self.loaded_plugins[plugin_name]
        
        try:
            # 创建模块 spec
            plugin_file_path = os.path.join(plugin_info['plugin_path'], f"{plugin_name}.py")
            spec = importlib.util.spec_from_file_location("plugin", plugin_file_path)
            plugin = importlib.util.module_from_spec(spec)
            # 执行模块代码
            spec.loader.exec_module(plugin)
            # 缓存已加载的插件
            self.loaded_plugins[plugin_name] = plugin
            return plugin
        except Exception as e:
            print(f"插件 {plugin_name} 加载失败: {e}")
            return None
    
    @staticmethod
    def get_plugin_config(plugin_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """获取插件配置
        
        参数:
            plugin_info (Dict[str, Any]): 插件信息
            
        返回值:
            Optional[Dict[str, Any]]: 插件配置，获取失败则返回None
        """
        try:
            config_path = os.path.join(plugin_info['plugin_path'], "config.toml")
            plugin_config: Dict[str, Any] = ConfigManager(
                config_path,
                create_if_not_exists=False
            ).config
            return plugin_config
        except FileNotFoundError:
            print(f"{plugin_info['plugin_name']}配置文件未找到，请检查文件路径。")
            return None
        except Exception as e:
            print(f"{plugin_info['plugin_name']}配置文件加载失败: {e}")
            return None
    
    def get_plugin_instance(self, plugin_info: Dict[str, Any]) -> Optional[PluginBase]:
        """获取或创建插件实例
        
        参数:
            plugin_info (Dict[str, Any]): 插件信息
            
        返回值:
            Optional[PluginBase]: 插件实例，获取失败则返回None
        """
        plugin_name = plugin_info['plugin_name']
        
        # 如果插件已经实例化，直接返回
        if plugin_name in self.plugin_instances:
            return self.plugin_instances[plugin_name]
        
        # 加载插件模块
        plugin_module = self.load_plugin(plugin_info)
        if not plugin_module:
            return None
        
        # 获取插件配置
        plugin_config = self.get_plugin_config(plugin_info)
        if not plugin_config:
            return None
        
        # 查找插件类（继承自PluginBase的类）
        plugin_class = None
        for name, obj in inspect.getmembers(plugin_module):
            if (inspect.isclass(obj)
                    and issubclass(obj, PluginBase)
                    and obj != PluginBase and obj != MenuPlugin
                    and obj != LastingPlugin and obj != InitPlugin):
                plugin_class = obj
                break
        
        if not plugin_class:
            print(f"插件 {plugin_name} 中找不到继承自PluginBase的类")
            return None
        
        # 创建插件实例
        try:
            plugin_instance = plugin_class(plugin_info, plugin_config)
            # 初始化插件
            if plugin_instance.initialize():
                # 缓存插件实例
                self.plugin_instances[plugin_name] = plugin_instance
                # 缓存插件类型
                if isinstance(plugin_instance, MenuPlugin):
                    self.plugin_types[plugin_name] = 'menu'
                elif isinstance(plugin_instance, LastingPlugin):
                    self.plugin_types[plugin_name] = 'lasting'
                elif isinstance(plugin_instance, InitPlugin):
                    self.plugin_types[plugin_name] = 'init'
                else:
                    self.plugin_types[plugin_name] = 'unknown'
                return plugin_instance
            else:
                print(f"插件 {plugin_name} 初始化失败")
                return None
        except Exception as e:
            print(f"插件 {plugin_name} 实例化失败: {e}")
            return None
    
    def execute_plugin_function(self, plugin_info: Dict[str, Any], function_name: str, *args, **kwargs) -> Any:
        """执行插件函数
        
        参数:
            plugin_info (Dict[str, Any]): 插件信息
            function_name (str): 函数名称
            *args, **kwargs: 传递给函数的参数
            
        返回值:
            Any: 函数执行结果
        """
        plugin_name = plugin_info['plugin_name']
        if plugin_info.get('plugin_type') == 'menu':
            plugin_instance = self.get_plugin_instance(plugin_info)
            if not plugin_instance:
                return None
            
            # 使用缓存的类型信息避免重复的类型检查
            if plugin_name in self.plugin_types and self.plugin_types[plugin_name] == 'menu':
                return plugin_instance.execute_function(function_name, *args)
            elif isinstance(plugin_instance, MenuPlugin):
                # 如果缓存中没有类型信息，则进行检查并缓存
                self.plugin_types[plugin_name] = 'menu'
                return plugin_instance.execute_function(function_name, *args)
            else:
                self.plugin_types[plugin_name] = 'unknown'
                print(f"插件 {plugin_name} 不是菜单型插件")
                return None

    def execute_lasting_plugins(self, parent):
        """执行持续性插件
        
        参数:
            parent: 父对象，通常是PetMain实例
        """
        for plugin_info in self.plugins:
            plugin_name = plugin_info['plugin_name']
            if not plugin_info.get('enabled', True) or plugin_info.get('plugin_type') != 'lasting':
                continue
                
            # 获取插件实例
            plugin_instance = self.get_plugin_instance(plugin_info)
            if not plugin_instance:
                continue
                
            # 使用缓存的类型信息避免重复的类型检查
            if plugin_name in self.plugin_types and self.plugin_types[plugin_name] == 'lasting':
                plugin_instance.update(parent)
            elif isinstance(plugin_instance, LastingPlugin):
                # 如果缓存中没有类型信息，则进行检查并缓存
                self.plugin_types[plugin_name] = 'lasting'
                plugin_instance.update(parent)
            else:
                self.plugin_types[plugin_name] = 'unknown'
                print(f"插件 {plugin_name} 不是持续性插件，忽略执行")
    
    def execute_init_plugins(self, parent):
        """执行初始化型插件
        
        在应用程序启动时调用，用于执行初始化型插件

        参数:
            parent: 父对象，通常是PetMain实例
        """
        for plugin_info in self.plugins:
            plugin_name = plugin_info['plugin_name']
            if not plugin_info.get('enabled', True) or plugin_info.get('plugin_type') != 'init':
                continue
                
            # 获取插件实例
            plugin_instance = self.get_plugin_instance(plugin_info)
            if not plugin_instance:
                continue
                
            # 使用缓存的类型信息避免重复的类型检查
            function_name = plugin_info.get('function_name', 'on_init')
            if plugin_name in self.plugin_types and self.plugin_types[plugin_name] == 'init':
                getattr(plugin_instance, function_name)(parent)
            elif isinstance(plugin_instance, InitPlugin):
                # 如果缓存中没有类型信息，则进行检查并缓存
                self.plugin_types[plugin_name] = 'init'
                getattr(plugin_instance, function_name)(parent)
            else:
                self.plugin_types[plugin_name] = 'unknown'
                print(f"插件 {plugin_name} 不是初始化型插件，忽略执行")
