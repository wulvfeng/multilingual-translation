"""
应用配置模块
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelConfig:
    """模型配置"""
    name: str = '../models'
    device: str = 'cpu'
    dtype: str = 'float32'
    max_length: int = 128
    max_length_generate: int = 150
    num_beams: int = 2
    low_cpu_mem_usage: bool = True


@dataclass
class ServerConfig:
    """服务器配置"""
    host: str = '0.0.0.0'
    port: int = 5000
    debug: bool = False
    allowed_ips: Optional[list] = None


@dataclass
class GUIConfig:
    """GUI配置"""
    window_title: str = 'Neural Translator Pro - 现代化多语言翻译系统'
    window_width: int = 1200
    window_height: int = 800
    theme: str = 'modern'


@dataclass
class AppConfig:
    """应用配置"""
    model: ModelConfig = None
    server: ServerConfig = None
    gui: GUIConfig = None
    
    def __post_init__(self):
        if self.model is None:
            self.model = ModelConfig()
        if self.server is None:
            self.server = ServerConfig()
        if self.gui is None:
            self.gui = GUIConfig()


class Config:
    """配置管理类"""
    
    _instance = None
    _config: Optional[AppConfig] = None
    
    @classmethod
    def get_instance(cls) -> 'Config':
        """获取配置单例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        if Config._instance is not None:
            raise Exception("Config类是单例，请使用get_instance()方法")
        self._config = AppConfig()
    
    @property
    def config(self) -> AppConfig:
        """获取应用配置"""
        return self._config
    
    @property
    def model_config(self) -> ModelConfig:
        """获取模型配置"""
        return self._config.model
    
    @property
    def server_config(self) -> ServerConfig:
        """获取服务器配置"""
        return self._config.server
    
    @property
    def gui_config(self) -> GUIConfig:
        """获取GUI配置"""
        return self._config.gui
    
    def update_model_config(self, **kwargs):
        """更新模型配置"""
        for key, value in kwargs.items():
            if hasattr(self._config.model, key):
                setattr(self._config.model, key, value)
    
    def update_server_config(self, **kwargs):
        """更新服务器配置"""
        for key, value in kwargs.items():
            if hasattr(self._config.server, key):
                setattr(self._config.server, key, value)
    
    def update_gui_config(self, **kwargs):
        """更新GUI配置"""
        for key, value in kwargs.items():
            if hasattr(self._config.gui, key):
                setattr(self._config.gui, key, value)
    
    def get_model_path(self) -> str:
        """获取模型路径"""
        model_name = self._config.model.name
        if os.path.isabs(model_name):
            return model_name
        
        # 相对路径，基于当前文件位置
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, '..', '..', model_name)
