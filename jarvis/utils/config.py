"""
Configuration module for Jarvis AI Assistant
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for Jarvis"""

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def load_config(self, config_path: str = "config.yaml") -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    self._config = yaml.safe_load(f) or {}
                logger.info(f"Configuration loaded from {config_path}")
            else:
                logger.warning(f"Config file not found: {config_path}")
                self._config = self._get_defaults()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._config = self._get_defaults()
        
        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self._config[key] = value

    @staticmethod
    def _get_defaults() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "jarvis": {
                "name": "Jarvis",
                "personality": "helpful",
                "voice_enabled": False
            },
            "agents": {
                "max_agents": 10,
                "auto_scaling": False
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }


# Singleton instance
config = Config()
