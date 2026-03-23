#!/usr/bin/env python3
"""
数据库连接测试脚本
按照software.md文档要求实现PostgreSQL连接测试
"""

import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """数据库管理器 - 按照software.md文档要求实现"""
    
    def __init__(self, host='localhost', port=5432, database='ecommerce_db', 
                 user='postgres', password='password'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.engine = None
    
    def connect(self):
        """建立数据库连接"""
        try:
            # 使用psycopg2连接
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            # 使用SQLAlchemy引擎
            connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(connection_string)
            
            logger.info("数据库连接成功")
            return True
            
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            return False
    
    def test_connection(self):
        """测试数据库连接"""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                logger.info(f"PostgreSQL版本: {version[0]}")
                
                cursor.execute("SELECT current_database();")
                db_name = cursor.fetchone()
                logger.info(f"当前数据库: {db_name[0]}")
                
                cursor.close()
                return True
            else:
                logger.error("数据库未连接")
                return False
                
        except Exception as e:
            logger.error(f"连接测试失败: {e}")
            return False
    
    def create_tables(self):
        """创建数据表"""
        try:
            cursor = self.connection.cursor()
            
            # 读取建表SQL
            with open('create_tables.sql', 'r', encoding='utf-8') as f:
                sql = f.read()
            
            cursor.execute(sql)
            self.connection.commit()
            
            logger.info("数据表创建成功")
            return True
            
        except Exception as e:
            logger.error(f"创建表失败: {e}")
            return False
    
    def insert_sample_data(self):
        """插入示例数据"""
        try:
            cursor = self.connection.cursor()
            
            # 读取初始化数据SQL
            with open('init_data.sql', 'r', encoding='utf-8') as f:
                sql = f.read()
            
            cursor.execute(sql)
            self.connection.commit()
            
            logger.info("示例数据插入成功")
            return True
            
        except Exception as e:
            logger.error(f"插入数据失败: {e}")
            return False
    
    def test_queries(self):
        """测试查询操作"""
        try:
            # 测试基本查询
            query1 = "SELECT COUNT(*) FROM products;"
            result1 = pd.read_sql(query1, self.engine)
            logger.info(f"商品总数: {result1.iloc[0, 0]}")
            
            # 测试分类统计
            query2 = """
            SELECT category, COUNT(*) as count, AVG(price) as avg_price
            FROM products 
            GROUP BY category 
            ORDER BY count DESC;
            """
            result2 = pd.read_sql(query2, self.engine)
            logger.info("分类统计:")
            logger.info(result2.to_string())
            
            # 测试用户交互统计
            query3 = """
            SELECT 
                p.title,
                COUNT(ui.id) as interaction_count,
                AVG(ui.rating) as avg_rating
            FROM products p
            LEFT JOIN user_interactions ui ON p.id = ui.product_id
            GROUP BY p.id, p.title
            ORDER BY interaction_count DESC
            LIMIT 5;
            """
            result3 = pd.read_sql(query3, self.engine)
            logger.info("热门商品:")
            logger.info(result3.to_string())
            
            return True
            
        except Exception as e:
            logger.error(f"查询测试失败: {e}")
            return False
    
    def test_recommendation_function(self):
        """测试推荐函数"""
        try:
            # 测试推荐函数
            query = "SELECT * FROM get_user_recommendations(1, 5);"
            result = pd.read_sql(query, self.engine)
            logger.info("用户推荐结果:")
            logger.info(result.to_string())
            
            return True
            
        except Exception as e:
            logger.error(f"推荐函数测试失败: {e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        try:
            if self.connection:
                self.connection.close()
            if self.engine:
                self.engine.dispose()
            logger.info("数据库连接已关闭")
        except Exception as e:
            logger.error(f"关闭连接失败: {e}")

def main():
    """主函数 - 按照software.md文档要求实现"""
    logger.info("开始数据库连接测试")
    
    # 创建数据库管理器
    db = DatabaseManager()
    
    try:
        # 连接数据库
        if not db.connect():
            logger.error("无法连接到数据库")
            return
        
        # 测试连接
        if not db.test_connection():
            logger.error("数据库连接测试失败")
            return
        
        # 创建表（如果不存在）
        if not db.create_tables():
            logger.error("创建表失败")
            return
        
        # 插入示例数据
        if not db.insert_sample_data():
            logger.error("插入示例数据失败")
            return
        
        # 测试查询
        if not db.test_queries():
            logger.error("查询测试失败")
            return
        
        # 测试推荐函数
        if not db.test_recommendation_function():
            logger.error("推荐函数测试失败")
            return
        
        logger.info("数据库测试完成，所有功能正常")
        
    except Exception as e:
        logger.error(f"数据库测试失败: {e}")
    
    finally:
        # 关闭连接
        db.close()

if __name__ == "__main__":
    main()
