#!/usr/bin/env python3
"""
TEMU爬虫系统日志模块
提供统一的日志记录功能
"""
import os
import logging
import logging.handlers
from datetime import datetime
from typing import Optional
from config import config

class CrawlerLogger:
    """爬虫日志记录器"""
    
    def __init__(self, name: str = "TEMUCrawler"):
        self.name = name
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger(self.name)
        logger.setLevel(getattr(logging, config.LOGGING_CONFIG["level"]))
        
        # 避免重复添加处理器
        if logger.handlers:
            return logger
        
        # 确保日志目录存在
        os.makedirs(config.PATHS["logs"], exist_ok=True)
        
        # 创建格式化器
        formatter = logging.Formatter(config.LOGGING_CONFIG["format"])
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 文件处理器（带轮转）
        log_file = config.get_log_file_path()
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=config.LOGGING_CONFIG["max_size"],
            backupCount=config.LOGGING_CONFIG["backup_count"],
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def info(self, message: str):
        """记录信息日志"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """记录调试日志"""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """记录警告日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """记录错误日志"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """记录严重错误日志"""
        self.logger.critical(message)
    
    def log_crawler_start(self, keyword: str, max_pages: int):
        """记录爬虫开始"""
        self.info(f"🚀 爬虫开始 - 关键词: {keyword}, 页数: {max_pages}")
    
    def log_crawler_end(self, success: bool, products_count: int, duration: float):
        """记录爬虫结束"""
        status = "成功" if success else "失败"
        self.info(f"🏁 爬虫结束 - 状态: {status}, 商品数: {products_count}, 耗时: {duration:.2f}秒")
    
    def log_page_inspection(self, url: str, is_valid: bool, message: str):
        """记录页面审查"""
        status = "✅ 通过" if is_valid else "❌ 失败"
        self.info(f"🔍 页面审查 - URL: {url}, 状态: {status}, 信息: {message}")
    
    def log_anti_detection(self, strategy: str, success: bool):
        """记录反爬检测处理"""
        status = "成功" if success else "失败"
        self.info(f"🛡️ 反爬处理 - 策略: {strategy}, 状态: {status}")
    
    def log_product_extraction(self, page: int, count: int):
        """记录商品提取"""
        self.info(f"📦 商品提取 - 第{page}页, 数量: {count}")
    
    def log_error(self, error_type: str, error_message: str, context: str = ""):
        """记录错误"""
        self.error(f"❌ 错误 - 类型: {error_type}, 消息: {error_message}, 上下文: {context}")
    
    def log_quality_analysis(self, total: int, valid_title: int, valid_price: int, quality_score: float):
        """记录数据质量分析"""
        self.info(f"📊 质量分析 - 总数: {total}, 有效标题: {valid_title}, 有效价格: {valid_price}, 质量分数: {quality_score:.1f}%")

# 创建全局日志记录器实例
logger = CrawlerLogger()

def get_logger(name: Optional[str] = None) -> CrawlerLogger:
    """获取日志记录器"""
    if name:
        return CrawlerLogger(name)
    return logger
