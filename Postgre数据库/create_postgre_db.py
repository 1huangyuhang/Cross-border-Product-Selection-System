#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL数据库创建脚本
此脚本用于创建PostgreSQL数据库和表结构，适用于爬虫项目的数据存储需求
"""

import psycopg2
import os
from psycopg2 import OperationalError

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'user': 'huangyuhang',  # macOS上Homebrew安装的PostgreSQL默认使用当前系统用户
    'password': '',      # 默认无密码，根据实际情况修改
    'dbname': 'postgres'  # 连接到默认的postgres数据库
}

# 要创建的数据库信息
NEW_DB_NAME = 'spider_db'  # 爬虫数据库名称

# 创建数据库函数
def create_database():
    """连接到PostgreSQL服务器并创建新数据库"""
    try:
        # 连接到默认的postgres数据库
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            dbname=DB_CONFIG['dbname']
        )
        conn.autocommit = True  # 允许创建数据库的SQL语句立即执行
        
        # 创建游标对象
        cursor = conn.cursor()
        
        # 检查数据库是否已存在
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (NEW_DB_NAME,))
        exists = cursor.fetchone()
        
        if exists:
            print(f"数据库 '{NEW_DB_NAME}' 已存在，跳过创建步骤。")
        else:
            # 创建新数据库
            cursor.execute(f"CREATE DATABASE {NEW_DB_NAME}")
            print(f"数据库 '{NEW_DB_NAME}' 创建成功！")
        
        # 关闭游标和连接
        cursor.close()
        conn.close()
        
    except OperationalError as e:
        print(f"无法连接到PostgreSQL服务器: {e}")
        print("请确认PostgreSQL服务已启动，且连接配置正确。")
        return False
    except Exception as e:
        print(f"创建数据库时发生错误: {e}")
        return False
    
    return True

# 创建表结构函数
def create_tables():
    """在新创建的数据库中创建表结构"""
    try:
        # 连接到新创建的数据库
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            dbname=NEW_DB_NAME
        )
        
        # 创建游标对象
        cursor = conn.cursor()
        
        # 读取并执行TEMU相关表的创建SQL
        sql_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'create_temu_related_tables.sql')
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        # 执行SQL脚本
        cursor.execute(sql_script)
        print("✅ TEMU相关数据表创建成功！")
        
        # 2. 创建爬虫任务表 - 记录爬虫执行情况
        create_tasks_table = """
        CREATE TABLE IF NOT EXISTS crawl_tasks (
            id SERIAL PRIMARY KEY,
            task_name VARCHAR(255) NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            status VARCHAR(50) DEFAULT 'pending',
            total_items INTEGER DEFAULT 0,
            success_items INTEGER DEFAULT 0,
            failed_items INTEGER DEFAULT 0,
            error_log TEXT
        )
        """
        cursor.execute(create_tasks_table)
        print("✅ 爬虫任务表 (crawl_tasks) 创建成功！")
        
        # 提交事务
        conn.commit()
        
        # 关闭游标和连接
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"创建表结构时发生错误: {e}")
        return False
    
    return True

# 主函数
def main():
    """主函数，协调整个数据库创建流程"""
    print("=== 开始创建PostgreSQL数据库 ===")
    
    # 1. 创建数据库
    if not create_database():
        print("数据库创建失败，程序终止。")
        return
    
    # 2. 创建表结构
    if not create_tables():
        print("表结构创建失败，程序终止。")
        return
    
    print("\n=== PostgreSQL数据库创建完成！ ===")
    print(f"数据库名称: {NEW_DB_NAME}")
    print(f"连接主机: {DB_CONFIG['host']}")
    print(f"连接端口: {DB_CONFIG['port']}")
    print("\n提示：如需修改数据库密码，可使用以下命令：")
    print(f"sudo -u postgres psql -c ""ALTER USER postgres WITH PASSWORD 'your_new_password';""")

if __name__ == "__main__":
    main()