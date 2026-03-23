# -*- coding: utf-8 -*-
"""
PostgreSQL数据库操作算法
用于查询和操作TEMU相关数据库表的功能实现
包含商品数据分析和趋势预测算法
"""

import psycopg2
from psycopg2 import OperationalError
from typing import List, Dict, Any
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import re
from collections import Counter
import math

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'user': 'huangyuhang',
    'password': '',
    'dbname': 'spider_db'
}

class DatabaseConnector:
    """数据库连接和操作类"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.conn = psycopg2.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                dbname=DB_CONFIG['dbname']
            )
            self.cursor = self.conn.cursor()
            return True
        except OperationalError as e:
            print(f"无法连接到PostgreSQL服务器: {e}")
            return False
    
    def disconnect(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def get_all_tables(self) -> List[str]:
        """获取数据库中所有的表名"""
        try:
            if not self.connect():
                return []
            
            self.cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            """)
            
            tables = self.cursor.fetchall()
            return [table[0] for table in tables]
        except Exception as e:
            print(f"获取表列表时出错: {e}")
            return []
        finally:
            self.disconnect()
    
    def get_table_structure(self, table_name: str) -> List[Dict[str, Any]]:
        """获取指定表的结构信息"""
        try:
            if not self.connect():
                return []
            
            self.cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s
                ORDER BY ordinal_position
            """, (table_name,))
            
            columns = self.cursor.fetchall()
            structure = []
            for col in columns:
                structure.append({
                    'name': col[0],
                    'type': col[1],
                    'nullable': col[2] == 'YES',
                    'default': col[3]
                })
            return structure
        except Exception as e:
            print(f"获取表结构时出错: {e}")
            return []
        finally:
            self.disconnect()
    
    def get_table_data(self, table_name: str, limit: int = 100) -> Dict[str, Any]:
        """获取指定表的数据"""
        try:
            if not self.connect():
                return {'columns': [], 'data': []}
            
            # 获取表结构
            structure = self.get_table_structure(table_name)
            if not structure:
                return {'columns': [], 'data': []}
            
            # 获取列名
            columns = [col['name'] for col in structure]
            
            # 查询数据
            self.connect()  # 重新连接，因为get_table_structure会关闭连接
            self.cursor.execute(f"SELECT * FROM {table_name} LIMIT %s", (limit,))
            data = self.cursor.fetchall()
            
            # 转换为字典列表
            result_data = []
            for row in data:
                row_dict = {}
                for i, col in enumerate(columns):
                    # 处理特殊类型
                    value = row[i]
                    if isinstance(value, (dict, list)):
                        # JSONB类型转换为字符串
                        value = str(value)
                    row_dict[col] = value
                result_data.append(row_dict)
            
            return {
                'columns': structure,
                'data': result_data
            }
        except Exception as e:
            print(f"获取表数据时出错: {e}")
            return {'columns': [], 'data': []}
        finally:
            self.disconnect()

# 实例化数据库连接器
db_connector = DatabaseConnector()

# 暴露的函数
def get_database_tables() -> List[str]:
    """获取数据库中所有表"""
    return db_connector.get_all_tables()


def get_table_details(table_name: str) -> Dict[str, Any]:
    """获取指定表的结构和数据"""
    return db_connector.get_table_data(table_name)


def get_temu_related_tables() -> List[str]:
    """获取所有TEMU相关的表"""
    all_tables = get_database_tables()
    return [table for table in all_tables if table.startswith('temu_')]


class ProductDataAnalyzer:
    """商品数据分析器"""
    
    def __init__(self):
        self.db_connector = DatabaseConnector()
    
    def clean_price_data(self, price_str: str) -> float:
        """清洗价格数据，提取数值"""
        if not price_str:
            return 0.0
        
        # 移除货币符号和空格
        price_clean = re.sub(r'[^\d.,]', '', str(price_str))
        
        # 处理不同格式的价格
        if ',' in price_clean and '.' in price_clean:
            # 格式如：1,234.56
            price_clean = price_clean.replace(',', '')
        elif ',' in price_clean:
            # 格式如：1,234 或 1,234,56
            parts = price_clean.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # 可能是 1,234.56 格式
                price_clean = price_clean.replace(',', '.')
            else:
                # 千位分隔符
                price_clean = price_clean.replace(',', '')
        
        try:
            return float(price_clean)
        except ValueError:
            return 0.0
    
    def clean_sales_data(self, sales_str: str) -> int:
        """清洗销量数据"""
        if not sales_str:
            return 0
        
        # 提取数字
        numbers = re.findall(r'\d+', str(sales_str))
        if numbers:
            return int(numbers[0])
        return 0
    
    def clean_rating_data(self, rating_str: str) -> float:
        """清洗评分数据"""
        if not rating_str:
            return 0.0
        
        # 提取评分数字
        rating_match = re.search(r'(\d+\.?\d*)', str(rating_str))
        if rating_match:
            rating = float(rating_match.group(1))
            # 如果评分大于5，可能是百分制，需要转换
            if rating > 5:
                rating = rating / 20  # 百分制转5分制
            return min(5.0, max(0.0, rating))
        return 0.0
    
    def extract_keywords(self, title: str) -> List[str]:
        """从商品标题中提取关键词"""
        if not title:
            return []
        
        # 简单的关键词提取（可以后续优化为更复杂的NLP算法）
        keywords = []
        
        # 移除常见停用词
        stop_words = {'的', '和', '与', '或', '在', '是', '有', '为', '用', 'for', 'and', 'or', 'with', 'in', 'on', 'at'}
        
        # 分割标题
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+|\d+', title.lower())
        
        for word in words:
            if len(word) > 1 and word not in stop_words:
                keywords.append(word)
        
        return keywords
    
    def analyze_price_trends(self, products: List[Dict]) -> Dict[str, Any]:
        """分析价格趋势"""
        if not products:
            return {}
        
        prices = []
        for product in products:
            price = self.clean_price_data(product.get('price', ''))
            if price > 0:
                prices.append(price)
        
        if not prices:
            return {}
        
        prices = np.array(prices)
        
        # 基础统计
        analysis = {
            'mean_price': float(np.mean(prices)),
            'median_price': float(np.median(prices)),
            'min_price': float(np.min(prices)),
            'max_price': float(np.max(prices)),
            'std_price': float(np.std(prices)),
            'price_range': float(np.max(prices) - np.min(prices)),
            'price_distribution': {
                'under_10': len([p for p in prices if p < 10]),
                '10_50': len([p for p in prices if 10 <= p < 50]),
                '50_100': len([p for p in prices if 50 <= p < 100]),
                'over_100': len([p for p in prices if p >= 100])
            }
        }
        
        # 价格趋势分析（如果有时间序列数据）
        if len(prices) > 1:
            # 简单的线性趋势
            x = np.arange(len(prices))
            coeffs = np.polyfit(x, prices, 1)
            analysis['trend_slope'] = float(coeffs[0])
            analysis['trend_direction'] = 'increasing' if coeffs[0] > 0 else 'decreasing'
        
        return analysis
    
    def analyze_sales_trends(self, products: List[Dict]) -> Dict[str, Any]:
        """分析销量趋势"""
        if not products:
            return {}
        
        sales_data = []
        for product in products:
            sales = self.clean_sales_data(product.get('sales', ''))
            if sales > 0:
                sales_data.append(sales)
        
        if not sales_data:
            return {}
        
        sales_data = np.array(sales_data)
        
        analysis = {
            'total_sales': int(np.sum(sales_data)),
            'avg_sales': float(np.mean(sales_data)),
            'median_sales': float(np.median(sales_data)),
            'max_sales': int(np.max(sales_data)),
            'sales_distribution': {
                'low_sales': len([s for s in sales_data if s < 100]),
                'medium_sales': len([s for s in sales_data if 100 <= s < 1000]),
                'high_sales': len([s for s in sales_data if s >= 1000])
            }
        }
        
        return analysis
    
    def analyze_rating_trends(self, products: List[Dict]) -> Dict[str, Any]:
        """分析评分趋势"""
        if not products:
            return {}
        
        ratings = []
        for product in products:
            rating = self.clean_rating_data(product.get('rating', ''))
            if rating > 0:
                ratings.append(rating)
        
        if not ratings:
            return {}
        
        ratings = np.array(ratings)
        
        analysis = {
            'avg_rating': float(np.mean(ratings)),
            'median_rating': float(np.median(ratings)),
            'min_rating': float(np.min(ratings)),
            'max_rating': float(np.max(ratings)),
            'rating_distribution': {
                'excellent': len([r for r in ratings if r >= 4.5]),
                'good': len([r for r in ratings if 3.5 <= r < 4.5]),
                'average': len([r for r in ratings if 2.5 <= r < 3.5]),
                'poor': len([r for r in ratings if r < 2.5])
            }
        }
        
        return analysis
    
    def analyze_keyword_trends(self, products: List[Dict]) -> Dict[str, Any]:
        """分析关键词趋势"""
        if not products:
            return {}
        
        all_keywords = []
        for product in products:
            title = product.get('title', '')
            keywords = self.extract_keywords(title)
            all_keywords.extend(keywords)
        
        if not all_keywords:
            return {}
        
        # 统计关键词频率
        keyword_counts = Counter(all_keywords)
        
        analysis = {
            'total_keywords': len(all_keywords),
            'unique_keywords': len(keyword_counts),
            'top_keywords': dict(keyword_counts.most_common(20)),
            'keyword_diversity': len(keyword_counts) / len(all_keywords) if all_keywords else 0
        }
        
        return analysis
    
    def predict_trends(self, products: List[Dict]) -> Dict[str, Any]:
        """预测商品趋势"""
        if not products:
            return {}
        
        # 基于价格和销量的趋势预测
        price_analysis = self.analyze_price_trends(products)
        sales_analysis = self.analyze_sales_trends(products)
        rating_analysis = self.analyze_rating_trends(products)
        
        predictions = {
            'market_opportunity': 'medium',
            'price_competitiveness': 'medium',
            'quality_indicators': 'medium',
            'recommendations': []
        }
        
        # 市场机会分析
        if sales_analysis.get('avg_sales', 0) > 500:
            predictions['market_opportunity'] = 'high'
            predictions['recommendations'].append('高销量商品，市场机会大')
        elif sales_analysis.get('avg_sales', 0) < 100:
            predictions['market_opportunity'] = 'low'
            predictions['recommendations'].append('销量较低，需要市场推广')
        
        # 价格竞争力分析
        if price_analysis.get('mean_price', 0) < 20:
            predictions['price_competitiveness'] = 'high'
            predictions['recommendations'].append('价格竞争力强')
        elif price_analysis.get('mean_price', 0) > 100:
            predictions['price_competitiveness'] = 'low'
            predictions['recommendations'].append('价格较高，需要优化成本')
        
        # 质量指标分析
        if rating_analysis.get('avg_rating', 0) > 4.0:
            predictions['quality_indicators'] = 'high'
            predictions['recommendations'].append('质量指标良好')
        elif rating_analysis.get('avg_rating', 0) < 3.0:
            predictions['quality_indicators'] = 'low'
            predictions['recommendations'].append('质量指标需要改善')
        
        return predictions
    
    def generate_chart_data(self, products: List[Dict]) -> Dict[str, Any]:
        """生成图表数据"""
        if not products:
            return {}
        
        # 价格分布图表数据
        prices = [self.clean_price_data(p.get('price', '')) for p in products if p.get('price')]
        prices = [p for p in prices if p > 0]
        
        # 销量分布图表数据
        sales = [self.clean_sales_data(p.get('sales', '')) for p in products if p.get('sales')]
        sales = [s for s in sales if s > 0]
        
        # 评分分布图表数据
        ratings = [self.clean_rating_data(p.get('rating', '')) for p in products if p.get('rating')]
        ratings = [r for r in ratings if r > 0]
        
        # 关键词云数据
        all_keywords = []
        for product in products:
            keywords = self.extract_keywords(product.get('title', ''))
            all_keywords.extend(keywords)
        keyword_counts = Counter(all_keywords)
        
        chart_data = {
            'price_distribution': {
                'labels': ['<$10', '$10-50', '$50-100', '>$100'],
                'data': [
                    len([p for p in prices if p < 10]),
                    len([p for p in prices if 10 <= p < 50]),
                    len([p for p in prices if 50 <= p < 100]),
                    len([p for p in prices if p >= 100])
                ]
            },
            'sales_distribution': {
                'labels': ['<100', '100-500', '500-1000', '>1000'],
                'data': [
                    len([s for s in sales if s < 100]),
                    len([s for s in sales if 100 <= s < 500]),
                    len([s for s in sales if 500 <= s < 1000]),
                    len([s for s in sales if s >= 1000])
                ]
            },
            'rating_distribution': {
                'labels': ['1-2星', '2-3星', '3-4星', '4-5星'],
                'data': [
                    len([r for r in ratings if 1 <= r < 2]),
                    len([r for r in ratings if 2 <= r < 3]),
                    len([r for r in ratings if 3 <= r < 4]),
                    len([r for r in ratings if 4 <= r <= 5])
                ]
            },
            'keyword_cloud': [
                {'text': word, 'weight': count} 
                for word, count in keyword_counts.most_common(30)
            ],
            'price_trend': {
                'labels': [f'商品{i+1}' for i in range(min(20, len(prices)))],
                'data': prices[:20]
            }
        }
        
        return chart_data
    
    def analyze_products(self, products: List[Dict]) -> Dict[str, Any]:
        """综合分析商品数据"""
        if not products:
            return {}
        
        analysis = {
            'basic_stats': {
                'total_products': len(products),
                'analysis_date': datetime.now().isoformat()
            },
            'price_analysis': self.analyze_price_trends(products),
            'sales_analysis': self.analyze_sales_trends(products),
            'rating_analysis': self.analyze_rating_trends(products),
            'keyword_analysis': self.analyze_keyword_trends(products),
            'predictions': self.predict_trends(products),
            'chart_data': self.generate_chart_data(products)
        }
        
        return analysis


# 创建分析器实例
product_analyzer = ProductDataAnalyzer()


def analyze_product_data(products: List[Dict]) -> Dict[str, Any]:
    """分析商品数据的公共接口"""
    return product_analyzer.analyze_products(products)


def get_analysis_chart_data(products: List[Dict]) -> Dict[str, Any]:
    """获取图表数据的公共接口"""
    return product_analyzer.generate_chart_data(products)