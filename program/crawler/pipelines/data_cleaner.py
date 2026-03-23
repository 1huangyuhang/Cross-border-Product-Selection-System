#!/usr/bin/env python3
"""
跨境电商选品系统 - 数据清洗管道
按照software.md文档要求实现数据清洗
"""

import re
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCleaner:
    """数据清洗器 - 按照software.md文档要求实现"""
    
    def __init__(self):
        self.price_pattern = re.compile(r'[\d,]+\.?\d*')
        self.rating_pattern = re.compile(r'[\d.]+')
        self.url_pattern = re.compile(r'https?://[^\s]+')
    
    def clean_product_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        清洗商品数据
        按照software.md文档要求实现数据清洗方法
        """
        try:
            cleaned_data = {}
            
            # 清洗标题
            cleaned_data['title'] = self._clean_text(raw_data.get('title', ''))
            
            # 清洗价格
            cleaned_data['price'] = self._clean_price(raw_data.get('price', ''))
            cleaned_data['original_price'] = self._clean_price(raw_data.get('original_price', ''))
            
            # 清洗评分
            cleaned_data['rating'] = self._clean_rating(raw_data.get('rating', ''))
            
            # 清洗数量
            cleaned_data['review_count'] = self._clean_number(raw_data.get('review_count', 0))
            cleaned_data['sales_count'] = self._clean_number(raw_data.get('sales_count', 0))
            
            # 清洗URL
            cleaned_data['product_url'] = self._clean_url(raw_data.get('product_url', ''))
            cleaned_data['image_url'] = self._clean_url(raw_data.get('image_url', ''))
            
            # 清洗分类和品牌
            cleaned_data['category'] = self._clean_text(raw_data.get('category', ''))
            cleaned_data['brand'] = self._clean_text(raw_data.get('brand', ''))
            
            # 清洗描述
            cleaned_data['description'] = self._clean_description(raw_data.get('description', ''))
            
            # 清洗关键词
            cleaned_data['keywords'] = self._clean_keywords(raw_data.get('keywords', ''))
            
            # 设置平台信息
            cleaned_data['platform'] = raw_data.get('platform', 'unknown')
            cleaned_data['platform_id'] = raw_data.get('platform_id', '')
            
            # 设置可用性
            cleaned_data['is_available'] = self._clean_boolean(raw_data.get('is_available', True))
            
            # 设置时间戳
            cleaned_data['crawl_date'] = datetime.now()
            cleaned_data['created_at'] = datetime.now()
            cleaned_data['updated_at'] = datetime.now()
            
            logger.info(f"数据清洗完成: {cleaned_data['title'][:50]}...")
            return cleaned_data
            
        except Exception as e:
            logger.error(f"数据清洗失败: {str(e)}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """清洗文本数据"""
        if not text:
            return ''
        
        # 去除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 限制长度
        return text[:500] if len(text) > 500 else text
    
    def _clean_price(self, price: str) -> Optional[float]:
        """清洗价格数据"""
        if not price:
            return None
        
        try:
            # 提取数字部分
            price_str = re.sub(r'[^\d.,]', '', str(price))
            if not price_str:
                return None
            
            # 处理千位分隔符
            price_str = price_str.replace(',', '')
            
            # 转换为浮点数
            return float(price_str)
        except (ValueError, TypeError):
            return None
    
    def _clean_rating(self, rating: str) -> Optional[float]:
        """清洗评分数据"""
        if not rating:
            return None
        
        try:
            # 提取数字
            rating_str = re.sub(r'[^\d.]', '', str(rating))
            if not rating_str:
                return None
            
            rating_value = float(rating_str)
            
            # 确保评分在0-5范围内
            if rating_value < 0:
                return 0.0
            elif rating_value > 5:
                return 5.0
            else:
                return rating_value
        except (ValueError, TypeError):
            return None
    
    def _clean_number(self, number: Any) -> int:
        """清洗数字数据"""
        if not number:
            return 0
        
        try:
            if isinstance(number, str):
                # 提取数字
                number_str = re.sub(r'[^\d]', '', str(number))
                return int(number_str) if number_str else 0
            else:
                return int(number)
        except (ValueError, TypeError):
            return 0
    
    def _clean_url(self, url: str) -> str:
        """清洗URL数据"""
        if not url:
            return ''
        
        # 验证URL格式
        if self.url_pattern.match(url):
            return url
        else:
            return ''
    
    def _clean_description(self, description: str) -> str:
        """清洗描述数据"""
        if not description:
            return ''
        
        # 去除HTML标签
        description = re.sub(r'<[^>]+>', '', description)
        
        # 去除多余空白
        description = re.sub(r'\s+', ' ', description).strip()
        
        # 限制长度
        return description[:2000] if len(description) > 2000 else description
    
    def _clean_keywords(self, keywords: str) -> str:
        """清洗关键词数据"""
        if not keywords:
            return ''
        
        # 分割关键词
        keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]
        
        # 去重并限制数量
        unique_keywords = list(dict.fromkeys(keyword_list))[:10]
        
        return ','.join(unique_keywords)
    
    def _clean_boolean(self, value: Any) -> bool:
        """清洗布尔值数据"""
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.lower() in ['true', '1', 'yes', 'available']
        else:
            return bool(value)
