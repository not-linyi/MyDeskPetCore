from abc import ABC, abstractmethod
from typing import Any, Dict


class PluginBase(ABC):
    """插件基类
    
    所有插件必须继承此基类，并实现相应的抽象方法。
    插件分为三种类型：
    1. 菜单型(menu)：在系统托盘菜单中添加菜单项，点击菜单项执行相应功能
    2. 持久型(lasting)：在每一帧更新时执行，用于实现持续性功能
    3. 初始化型(init)：在应用程序启动时执行一次，用于初始化功能
    
    属性:
        plugin_info (Dict[str, Any]): 插件信息
        plugin_config (Dict[str, Any]): 插件配置
    """

    def __init__(self, plugin_info: Dict[str, Any], plugin_config: Dict[str, Any]):
        """初始化插件基类
        
        参数:
            plugin_info (Dict[str, Any]): 插件信息
            plugin_config (Dict[str, Any]): 插件配置
        """
        self.plugin_info = plugin_info
        self.plugin_config = plugin_config

    @abstractmethod
    def initialize(self) -> bool:
        """初始化插件
        
        在插件加载时调用，用于初始化插件资源
        
        返回值:
            bool: 初始化是否成功
        """
        pass

    def cleanup(self) -> None:
        """清理插件资源
        
        在插件卸载时调用，用于清理插件资源
        """
        pass


class MenuPlugin(PluginBase):
    """菜单型插件基类
    
    在系统托盘菜单中添加菜单项，点击菜单项执行相应功能
    
    菜单型插件配置示例:
    ```toml
    [plugin]
    name = "示例菜单插件"
    icon = "HOME_FILL"
    
    [[menu]]
    menu_name = "菜单项1"
    menu_icon = "path/to/icon.png"
    function_name = "function1"
    menu_parameter = "参数1"
    
    [[menu]]
    menu_name = "菜单项2"
    menu_icon = "path/to/icon.png"
    function_name = "function2"
    menu_parameter = "参数2"
    ```
    
    插件可以通过实现create_custom_menu方法来自定义菜单，该方法将覆盖配置文件中的菜单项
    """

    def initialize(self) -> bool:
        """初始化菜单型插件
        
        菜单型插件通常不需要特殊初始化，直接返回True
        
        返回值:
            bool: 初始化是否成功
        """
        return True

    def execute_function(self, function_name: str, parameter: Any) -> Any:
        """执行函数
        
        参数:
            function_name (str): 函数名称
            parameter (Any): 函数参数
            
        返回值:
            Any: 函数执行结果
        """
        if hasattr(self, function_name):
            return getattr(self, function_name)(parameter)
        return None
        
    def create_custom_menu(self, plugin_access):
        """创建自定义菜单
        
        插件可以重写此方法来创建自定义菜单
        
        参数:
            plugin_access: 插件自定义菜单
            
        返回值:
            bool: 是否已创建自定义菜单，True表示已创建，False表示使用默认的菜单模式
        """
        return False


class LastingPlugin(PluginBase):
    """持久型插件基类
    
    在每一帧更新时执行，用于实现持续性功能
    
    持久型插件配置示例:
    ```toml
    [plugin]
    name = "示例持久型插件"
    function_name = "update"
    ```
    """

    def initialize(self) -> bool:
        """初始化持久型插件
        
        返回值:
            bool: 初始化是否成功
        """
        return True

    @abstractmethod
    def update(self, parent) -> None:
        """更新方法，在每一帧调用
        
        参数:
            parent: 父对象，通常是PetMain实例
        """
        pass


class InitPlugin(PluginBase):
    """初始化型插件基类
    
    在应用程序启动时执行一次，用于初始化功能
    
    初始化型插件配置示例:
    ```toml
    [plugin]
    name = "示例初始化型插件"
    function_name = "on_init"  # 初始化时调用的函数名
    ```
    """

    def initialize(self) -> bool:
        """初始化插件并执行初始化函数
        
        返回值:
            bool: 初始化是否成功
        """
        function_name = self.plugin_info.get('function_name', 'on_init')
        if hasattr(self, function_name):
            try:
                getattr(self, function_name)()
                return True
            except Exception as e:
                print(f"初始化型插件 {self.plugin_info['plugin_name']} 执行函数 {function_name} 失败: {e}")
                return False
        return False

    def on_init(self) -> None:
        """默认的初始化函数
        
        在应用程序启动时执行一次
        """
        pass
