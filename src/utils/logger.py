#!/usr/bin/env python3
"""
日志工具 - 快乐魔仙数字货币分析技能
"""

import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = "happy_fairy_crypto_analysis",
    level: str = "INFO",
    log_file: Optional[str] = None,
    max_size: str = "10MB",
    backup_count: int = 5
) -> logging.Logger:
    """
    设置日志器
    
    Args:
        name: 日志器名称
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日志文件路径，如果为None则只输出到控制台
        max_size: 日志文件最大大小 (如: "10MB", "100KB")
        backup_count: 备份文件数量
    
    Returns:
        logging.Logger: 配置好的日志器
    """
    # 创建日志器
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定了日志文件）
    if log_file:
        try:
            # 确保日志目录存在
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 创建轮转文件处理器
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=_parse_size(max_size),
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            logger.info(f"日志文件已配置: {log_file}")
            
        except Exception as e:
            logger.warning(f"无法创建日志文件处理器: {e}")
    
    return logger

def _parse_size(size_str: str) -> int:
    """解析大小字符串为字节数"""
    size_str = size_str.upper().strip()
    
    if size_str.endswith('KB'):
        return int(float(size_str[:-2]) * 1024)
    elif size_str.endswith('MB'):
        return int(float(size_str[:-2]) * 1024 * 1024)
    elif size_str.endswith('GB'):
        return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
    elif size_str.endswith('TB'):
        return int(float(size_str[:-2]) * 1024 * 1024 * 1024 * 1024)
    else:
        # 假设是字节数
        try:
            return int(size_str)
        except ValueError:
            return 10 * 1024 * 1024  # 默认10MB

def get_logger(name: str = "happy_fairy_crypto_analysis") -> logging.Logger:
    """获取日志器（单例模式）"""
    return logging.getLogger(name)

class LogContext:
    """日志上下文管理器"""
    
    def __init__(self, logger: logging.Logger, message: str, level: str = "INFO"):
        self.logger = logger
        self.message = message
        self.level = level.upper()
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        log_method = getattr(self.logger, self.level.lower(), self.logger.info)
        log_method(f"开始: {self.message}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        status = "完成" if exc_type is None else "失败"
        
        log_method = getattr(self.logger, self.level.lower(), self.logger.info)
        log_method(f"{status}: {self.message} (耗时: {elapsed:.2f}秒)")
        
        if exc_type is not None:
            self.logger.error(f"错误详情: {exc_val}", exc_info=True)
        
        # 不捕获异常，让上层处理
        return False

# 导入time模块
import time