#!/usr/bin/env python3
"""
TEMU爬虫系统配置文件
统一管理所有配置参数
"""
import os
from typing import Dict, List

class Config:
    """配置类"""
    
    # 基础配置
    PROJECT_NAME = "TEMU跨境电商选品爬虫系统"
    VERSION = "2.0.0"
    
    # 默认搜索参数
    DEFAULT_KEYWORD = "手机配件"
    DEFAULT_MAX_PAGES = 3
    DEFAULT_MAX_PRODUCTS_PER_PAGE = 20
    
    # 浏览器配置
    BROWSER_CONFIG = {
        "headless": False,
        "debug": True,
        "window_size": (1920, 1080),
        "page_load_timeout": 30,
        "implicit_wait": 10,
        "script_timeout": 30
    }
    
    # 反爬虫配置
    ANTI_DETECTION_CONFIG = {
        "max_retry_attempts": 3,
        "retry_delay": 5,
        "search_timeout": 30,
        "page_load_timeout": 20,
        "scroll_delay": 2,
        "type_delay": (0.1, 0.3)
    }
    
    # 用户代理列表
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    ]
    
    # 搜索框选择器
    SEARCH_SELECTORS = [
        'input[type="search"]',
        'input[placeholder*="搜索"]',
        'input[placeholder*="search"]',
        '#searchInput',
        'input[role="searchbox"]',
        'input[name="search"]',
        'input[id*="search"]',
        'input[class*="search"]'
    ]
    
    # 商品元素选择器
    PRODUCT_SELECTORS = [
        '[data-testid*="product"]',
        '.product-item',
        '.goods-item',
        '[class*="product"]',
        '[class*="item"]',
        'a[href*="/product/"]',
        'a[href*="/goods/"]',
        'div[class*="card"]',
        'div[class*="container"]',
        'article',
        'section',
        'div[role="listitem"]',
        'li[class*="item"]',
        'div[class*="grid"] > div',
        'div[class*="row"] > div'
    ]
    
    # 安全验证检测关键词
    SECURITY_VERIFICATION_INDICATORS = [
        '安全验证', 'security', 'verification', 'captcha', '验证'
    ]
    
    # 反爬系统检测关键词
    ANTI_BOT_INDICATORS = [
        'access denied', 'blocked', 'forbidden', 'rate limit',
        'too many requests', 'suspicious activity',
        '访问被拒绝', '被阻止', '请求过多', '可疑活动'
    ]
    
    # 空结果检测关键词
    EMPTY_INDICATORS = [
        'no results', 'no products', 'not found', 'empty',
        '无结果', '没有找到', '暂无商品', '没有相关商品'
    ]
    
    # 文件路径配置
    PATHS = {
        "results": "results",
        "logs": "logs", 
        "data": "data",
        "temp": "temp"
    }
    
    # 日志配置
    LOGGING_CONFIG = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/crawler.log",
        "max_size": 10 * 1024 * 1024,  # 10MB
        "backup_count": 5
    }
    
    # 代理配置（可选）
    PROXY_CONFIG = {
        "enabled": False,
        "proxies": [],
        "rotation": True
    }
    
    # 数据质量阈值
    QUALITY_THRESHOLDS = {
        "min_title_length": 5,
        "min_price_length": 1,
        "required_fields": ["title", "price"],
        "quality_score_threshold": 60
    }
    
    @classmethod
    def get_user_agent(cls) -> str:
        """获取随机用户代理"""
        import random
        return random.choice(cls.USER_AGENTS)
    
    @classmethod
    def ensure_directories(cls):
        """确保必要的目录存在"""
        for path in cls.PATHS.values():
            os.makedirs(path, exist_ok=True)
    
    @classmethod
    def get_log_file_path(cls) -> str:
        """获取日志文件路径"""
        return os.path.join(cls.PATHS["logs"], "crawler.log")
    
    @classmethod
    def get_results_path(cls) -> str:
        """获取结果保存路径"""
        return cls.PATHS["results"]

# 创建全局配置实例
config = Config()
