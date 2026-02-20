#!/usr/bin/env python3
"""
配置加载器 - 快乐魔仙数字货币分析技能
"""

import os
import yaml
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigLoader:
    """配置加载器"""
    
    DEFAULT_CONFIG = {
        'api': {
            'coingecko': {
                'enabled': True,
                'api_key': '',  # 可选API密钥
                'cache_ttl': 300  # 缓存时间(秒)
            }
        },
        'currencies': [
            {
                'symbol': 'BTC',
                'name': 'Bitcoin',
                'coin_id': 'bitcoin',
                'enabled': True
            },
            {
                'symbol': 'ETH',
                'name': 'Ethereum',
                'coin_id': 'ethereum',
                'enabled': True
            }
        ],
        'analysis': {
            'default_timeframe': '2h',
            'indicators': {
                'ma': {
                    'periods': [5, 48, 180],
                    'enabled': True
                },
                'macd': {
                    'fast': 6,
                    'slow': 7,
                    'signal': 6,
                    'enabled': True
                },
                'kdj': {
                    'period': 9,
                    'k_period': 3,
                    'd_period': 3,
                    'enabled': True
                },
                'skdj': {
                    'period': 9,
                    'k_period': 3,
                    'd_period': 3,
                    'enabled': True
                },
                'obv': {
                    'period': 30,
                    'enabled': True
                },
                'td': {
                    'buy_count': 9,
                    'sell_count': 13,
                    'enabled': True
                }
            }
        },
        'notification': {
            'enabled': True,
            'telegram': {
                'enabled': True,
                'bot_token': '',  # 需要用户配置
                'chat_id': ''     # 需要用户配置
            },
            'interval': 60,      # 检查间隔(秒)
            'cooldown': 300      # 同一币种冷却时间(秒)
        },
        'monitoring': {
            'enabled': True,
            'check_interval': 60,
            'alert_threshold': 1.0  # 价格变化警报阈值(%)
        },
        'logging': {
            'level': 'INFO',
            'file': 'logs/analysis.log',
            'max_size': '10MB',
            'backup_count': 5
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化配置加载器"""
        self.config_path = config_path or self._find_config_path()
        self.config = self.DEFAULT_CONFIG.copy()
        self.loaded = False
        
        logger.info(f"配置加载器初始化，配置路径: {self.config_path}")
    
    def _find_config_path(self) -> str:
        """查找配置文件路径"""
        # 可能的配置文件路径
        possible_paths = [
            # 1. 用户主目录
            os.path.expanduser('~/.happy-fairy-crypto-analysis/config.yaml'),
            # 2. 当前工作目录
            './config.yaml',
            # 3. 技能目录
            os.path.join(os.path.dirname(__file__), '../../config/config.yaml'),
            # 4. 默认位置
            '/etc/happy-fairy-crypto-analysis/config.yaml'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"找到配置文件: {path}")
                return path
        
        # 没有找到现有配置文件，使用默认位置
        default_path = os.path.expanduser('~/.happy-fairy-crypto-analysis/config.yaml')
        logger.info(f"未找到现有配置文件，使用默认位置: {default_path}")
        return default_path
    
    def load(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f) or {}
                
                # 深度合并配置
                self._deep_merge(self.config, user_config)
                logger.info(f"配置文件加载成功: {self.config_path}")
            else:
                logger.warning(f"配置文件不存在，使用默认配置: {self.config_path}")
                # 创建配置文件目录
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                
                # 保存默认配置
                self.save()
                logger.info(f"已创建默认配置文件: {self.config_path}")
            
            self.loaded = True
            self._validate_config()
            
            return self.config
            
        except yaml.YAMLError as e:
            logger.error(f"配置文件YAML格式错误: {e}")
            raise
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            raise
    
    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """深度合并两个字典"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                # 递归合并字典
                self._deep_merge(base[key], value)
            else:
                # 直接替换或添加
                base[key] = value
        return base
    
    def _validate_config(self):
        """验证配置"""
        errors = []
        
        # 验证必填字段
        if self.config['notification']['enabled']:
            telegram_config = self.config['notification']['telegram']
            if telegram_config['enabled']:
                if not telegram_config.get('bot_token'):
                    errors.append("Telegram Bot Token未配置")
                if not telegram_config.get('chat_id'):
                    errors.append("Telegram Chat ID未配置")
        
        # 验证技术指标配置
        indicators = self.config['analysis']['indicators']
        for indicator_name, indicator_config in indicators.items():
            if indicator_config.get('enabled', False):
                # 这里可以添加特定指标的验证逻辑
                pass
        
        if errors:
            error_msg = "配置验证失败:\n" + "\n".join(f"  - {error}" for error in errors)
            logger.warning(error_msg)
            # 不抛出异常，只是记录警告
    
    def save(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """保存配置文件"""
        try:
            config_to_save = config or self.config
            
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_to_save, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            logger.info(f"配置文件保存成功: {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        if not self.loaded:
            self.load()
        
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置值"""
        if not self.loaded:
            self.load()
        
        keys = key.split('.')
        config_ref = self.config
        
        try:
            # 导航到父级
            for k in keys[:-1]:
                if k not in config_ref:
                    config_ref[k] = {}
                config_ref = config_ref[k]
            
            # 设置值
            config_ref[keys[-1]] = value
            
            # 保存到文件
            return self.save()
            
        except Exception as e:
            logger.error(f"设置配置值失败: {e}")
            return False
    
    def get_currency_config(self, symbol: str) -> Optional[Dict[str, Any]]:
        """获取币种配置"""
        currencies = self.get('currencies', [])
        for currency in currencies:
            if currency.get('symbol') == symbol and currency.get('enabled', False):
                return currency
        return None
    
    def get_enabled_currencies(self) -> List[Dict[str, Any]]:
        """获取启用的币种列表"""
        currencies = self.get('currencies', [])
        return [c for c in currencies if c.get('enabled', False)]
    
    def get_telegram_config(self) -> Optional[Dict[str, Any]]:
        """获取Telegram配置"""
        notification = self.get('notification', {})
        if notification.get('enabled', False):
            telegram = notification.get('telegram', {})
            if telegram.get('enabled', False):
                return telegram
        return None
    
    def is_telegram_enabled(self) -> bool:
        """检查Telegram是否启用"""
        telegram_config = self.get_telegram_config()
        return bool(telegram_config and telegram_config.get('bot_token') and telegram_config.get('chat_id'))
    
    def create_config_template(self, output_path: str) -> bool:
        """创建配置模板"""
        try:
            template = {
                'happy_fairy_crypto_analysis': self.DEFAULT_CONFIG
            }
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# 快乐魔仙数字货币分析技能配置\n")
                f.write("# 请根据您的需求修改以下配置\n\n")
                yaml.dump(template, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            logger.info(f"配置模板创建成功: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"创建配置模板失败: {e}")
            return False