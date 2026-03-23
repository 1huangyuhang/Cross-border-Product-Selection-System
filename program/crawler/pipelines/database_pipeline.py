#!/usr/bin/env python3
"""
跨境电商选品系统 - 数据库存储管道
按照software.md文档要求实现数据存储
"""

import logging
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabasePipeline:
    """数据库存储管道 - 按照software.md文档要求实现"""
    
    def __init__(self, connection_string: str = None):
        """
        初始化数据库连接
        按照software.md文档要求使用PostgreSQL
        """
        self.connection_string = connection_string or \
            "postgresql://postgres:password@localhost:5432/ecommerce_db"
        
        try:
            self.engine = create_engine(self.connection_string)
            logger.info("数据库连接初始化成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            raise
    
    def save_product(self, product_data: Dict[str, Any]) -> bool:
        """
        保存单个商品数据
        按照software.md文档要求实现数据存储
        """
        try:
            # 检查商品是否已存在
            if self._product_exists(product_data.get('platform_id'), product_data.get('platform')):
                logger.info(f"商品已存在，跳过: {product_data.get('title', '')[:50]}")
                return True
            
            # 构建插入SQL
            insert_sql = """
                INSERT INTO products (
                    title, price, original_price, rating, review_count, sales_count,
                    product_url, image_url, category, brand, description, keywords,
                    platform, platform_id, is_available, crawl_date, created_at, updated_at
                ) VALUES (
                    :title, :price, :original_price, :rating, :review_count, :sales_count,
                    :product_url, :image_url, :category, :brand, :description, :keywords,
                    :platform, :platform_id, :is_available, :crawl_date, :created_at, :updated_at
                )
            """
            
            # 执行插入
            with self.engine.connect() as conn:
                conn.execute(text(insert_sql), product_data)
                conn.commit()
            
            logger.info(f"商品保存成功: {product_data.get('title', '')[:50]}")
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"商品保存失败: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"数据库操作异常: {str(e)}")
            return False
    
    def save_products_batch(self, products_data: List[Dict[str, Any]]) -> int:
        """
        批量保存商品数据
        按照software.md文档要求实现批量存储
        """
        success_count = 0
        
        try:
            for product_data in products_data:
                if self.save_product(product_data):
                    success_count += 1
            
            logger.info(f"批量保存完成: {success_count}/{len(products_data)} 成功")
            return success_count
            
        except Exception as e:
            logger.error(f"批量保存失败: {str(e)}")
            return success_count
    
    def _product_exists(self, platform_id: str, platform: str) -> bool:
        """检查商品是否已存在"""
        try:
            check_sql = """
                SELECT COUNT(*) FROM products 
                WHERE platform_id = :platform_id AND platform = :platform
            """
            
            with self.engine.connect() as conn:
                result = conn.execute(text(check_sql), {
                    'platform_id': platform_id,
                    'platform': platform
                })
                count = result.scalar()
                return count > 0
                
        except Exception as e:
            logger.error(f"检查商品存在性失败: {str(e)}")
            return False
    
    def get_products_count(self) -> int:
        """获取商品总数"""
        try:
            count_sql = "SELECT COUNT(*) FROM products"
            
            with self.engine.connect() as conn:
                result = conn.execute(text(count_sql))
                return result.scalar()
                
        except Exception as e:
            logger.error(f"获取商品数量失败: {str(e)}")
            return 0
    
    def get_products_by_category(self, category: str, limit: int = 100) -> List[Dict[str, Any]]:
        """根据分类获取商品"""
        try:
            query_sql = """
                SELECT * FROM products 
                WHERE category = :category 
                ORDER BY created_at DESC 
                LIMIT :limit
            """
            
            with self.engine.connect() as conn:
                result = conn.execute(text(query_sql), {
                    'category': category,
                    'limit': limit
                })
                
                products = []
                for row in result:
                    products.append(dict(row._mapping))
                
                return products
                
        except Exception as e:
            logger.error(f"获取分类商品失败: {str(e)}")
            return []
    
    def update_product_availability(self, platform_id: str, platform: str, is_available: bool) -> bool:
        """更新商品可用性"""
        try:
            update_sql = """
                UPDATE products 
                SET is_available = :is_available, updated_at = :updated_at
                WHERE platform_id = :platform_id AND platform = :platform
            """
            
            with self.engine.connect() as conn:
                conn.execute(text(update_sql), {
                    'is_available': is_available,
                    'updated_at': datetime.now(),
                    'platform_id': platform_id,
                    'platform': platform
                })
                conn.commit()
            
            logger.info(f"商品可用性更新成功: {platform_id}")
            return True
            
        except Exception as e:
            logger.error(f"更新商品可用性失败: {str(e)}")
            return False
    
    def cleanup_old_data(self, days: int = 30) -> int:
        """清理过期数据"""
        try:
            cleanup_sql = """
                DELETE FROM products 
                WHERE created_at < NOW() - INTERVAL '%s days'
            """ % days
            
            with self.engine.connect() as conn:
                result = conn.execute(text(cleanup_sql))
                conn.commit()
                deleted_count = result.rowcount
            
            logger.info(f"清理过期数据完成: 删除了 {deleted_count} 条记录")
            return deleted_count
            
        except Exception as e:
            logger.error(f"清理过期数据失败: {str(e)}")
            return 0
    
    def close_connection(self):
        """关闭数据库连接"""
        try:
            if hasattr(self, 'engine'):
                self.engine.dispose()
            logger.info("数据库连接已关闭")
        except Exception as e:
            logger.error(f"关闭数据库连接失败: {str(e)}")
