#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证所有TEMU相关表是否成功创建
"""

import psycopg2
from psycopg2 import OperationalError

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'user': 'huangyuhang',
    'password': '',  # 请在这里填写您的PostgreSQL密码
    'dbname': 'spider_db'
}

def verify_all_tables():
    """验证所有TEMU相关表是否成功创建"""
    try:
        # 连接到数据库
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            dbname=DB_CONFIG['dbname']
        )
        
        print("✅ 数据库连接成功！")
        
        # 创建游标对象
        cursor = conn.cursor()
        
        # 列出所有应该创建的表
        expected_tables = [
            'temu_category',
            'temu_product_demand',
            'temu_product_competition',
            'temu_product_profit',
            'temu_product_feedback',
            'temu_product_base'  # 之前创建的基础表
        ]
        
        # 查询数据库中的所有表
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        print(f"\n📊 spider_db数据库中的表: ")
        for table in existing_tables:
            print(f"   - {table}")
        
        # 检查所有预期的表是否都已创建
        print(f"\n✅ 表创建验证结果: ")
        all_tables_exist = True
        
        for table in expected_tables:
            if table in existing_tables:
                print(f"   ✅ {table} - 已成功创建")
                
                # 显示表结构（字段名和数据类型）
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = %s 
                    ORDER BY ordinal_position
                """, (table,))
                
                columns = cursor.fetchall()
                print(f"     字段列表: ")
                for column in columns:
                    print(f"        - {column[0]} ({column[1]})")
                
                # 显示表的索引
                cursor.execute("""
                    SELECT indexname 
                    FROM pg_indexes 
                    WHERE tablename = %s
                """, (table,))
                
                indexes = cursor.fetchall()
                if indexes:
                    print(f"     索引列表: ")
                    for index in indexes:
                        print(f"        - {index[0]}")
                else:
                    print(f"     索引列表: 无")
                
                print()  # 空行分隔不同的表
            else:
                print(f"   ❌ {table} - 创建失败")
                all_tables_exist = False
        
        # 关闭游标和连接
        cursor.close()
        conn.close()
        
        if all_tables_exist:
            print("✅ 所有预期的表都已成功创建！")
        else:
            print("❌ 有部分表创建失败，请检查SQL文件和错误信息。")
        
        return all_tables_exist
        
    except OperationalError as e:
        print(f"❌ 无法连接到PostgreSQL数据库: {e}")
        print("提示：请检查以下几点：")
        print("1. PostgreSQL服务是否正在运行")
        print("2. 数据库密码是否已在脚本中正确填写")
        print("3. 连接配置是否正确")
        return False
    except Exception as e:
        print(f"❌ 验证过程中发生错误: {e}")
        return False

def main():
    """主函数"""
    print("=== 开始TEMU相关表验证 ===")
    
    # 执行表验证
    if verify_all_tables():
        print("\n=== TEMU相关表验证成功！ ===")
        print("所有表已成功创建，可以开始在爬虫代码中使用这些表存储数据。")
        print("\n表结构说明：")
        print("1. temu_category - 品类配置表（存储品类信息和佣金率）")
        print("2. temu_product_base - 商品基础信息表（存储商品核心信息）")
        print("3. temu_product_demand - 市场需求数据表（存储销量、收藏量等数据）")
        print("4. temu_product_competition - 产品竞争力数据表（存储竞品信息）")
        print("5. temu_product_profit - 价格利润数据表（存储价格和利润计算）")
        print("6. temu_product_feedback - 买家反馈数据表（存储评分和评论信息）")
    else:
        print("\n=== TEMU相关表验证失败！ ===")

if __name__ == "__main__":
    main()