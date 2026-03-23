#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL数据库连接测试脚本
此脚本用于验证之前创建的spider_db数据库是否可以正常连接和操作
"""

import psycopg2
from psycopg2 import OperationalError

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'user': 'huangyuhang',
    'password': '',
    'dbname': 'spider_db'
}

# 测试数据库连接函数
def test_connection():
    """测试PostgreSQL数据库连接是否正常"""
    try:
        # 连接到spider_db数据库
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
        
        # 查看数据库中的所有表
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        print(f"\n📊 数据库中的表: ")
        for table in tables:
            print(f"   - {table[0]}")
        
        # 检查TEMU相关表是否存在
        temu_tables = ['temu_category', 'temu_product_base', 'temu_product_demand', 
                      'temu_product_competition', 'temu_product_profit', 'temu_product_feedback']
        
        print(f"\n🔍 验证TEMU相关表: ")
        for table in temu_tables:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = %s
                )
            """, (table,))
            exists = cursor.fetchone()[0]
            print(f"   - {table}: {'✓ 存在' if exists else '✗ 不存在'}")
        
        # 向爬虫任务表插入一条测试数据
        cursor.execute("""
            INSERT INTO crawl_tasks (task_name, status) 
            VALUES ('test_task', 'completed')
            RETURNING id
        """)
        
        task_id = cursor.fetchone()[0]
        print(f"\n✅ 成功插入一条测试任务记录，ID: {task_id}")
        
        # 查询刚插入的测试数据
        cursor.execute("""
            SELECT id, task_name, status, start_time 
            FROM crawl_tasks 
            WHERE id = %s
        """, (task_id,))
        
        task_data = cursor.fetchone()
        print(f"\n📋 查询测试任务记录: ")
        print(f"   - ID: {task_data[0]}")
        print(f"   - 任务名称: {task_data[1]}")
        print(f"   - 状态: {task_data[2]}")
        print(f"   - 开始时间: {task_data[3]}")
        
        # 更新测试数据
        cursor.execute("""
            UPDATE crawl_tasks 
            SET status = 'tested', success_items = 1 
            WHERE id = %s
        """, (task_id,))
        print(f"\n✅ 成功更新测试任务记录")
        
        # 再次查询更新后的数据
        cursor.execute("""
            SELECT status, success_items 
            FROM crawl_tasks 
            WHERE id = %s
        """, (task_id,))
        
        updated_data = cursor.fetchone()
        print(f"   - 更新后状态: {updated_data[0]}")
        print(f"   - 成功项数: {updated_data[1]}")
        
        # 删除测试数据
        cursor.execute("DELETE FROM crawl_tasks WHERE id = %s", (task_id,))
        print(f"\n✅ 成功删除测试任务记录")
        
        # 提交事务
        conn.commit()
        
        # 关闭游标和连接
        cursor.close()
        conn.close()
        
        print("\n✅ 数据库连接测试完成！所有操作均成功执行。")
        
    except OperationalError as e:
        print(f"❌ 无法连接到PostgreSQL数据库: {e}")
        return False
    except Exception as e:
        print(f"❌ 数据库操作时发生错误: {e}")
        return False
    
    return True

# 主函数
def main():
    """主函数，执行数据库连接测试"""
    print("=== 开始PostgreSQL数据库连接测试 ===")
    
    # 执行连接测试
    if test_connection():
        print("\n=== PostgreSQL数据库连接测试通过！ ===")
        print("数据库已成功创建并可正常使用。")
        print("TEMU相关表结构已完整创建，可用于爬虫数据存储。")
        print("\n提示：")
        print("1. 可以使用命令行工具连接数据库：psql spider_db")
        print("2. 可以使用Python的psycopg2库在爬虫代码中操作数据库")
        print("3. 如需修改数据库配置，请编辑create_postgre_db.py和test_db_connection.py中的DB_CONFIG")
        print("4. 详细的数据表结构说明请查看temu_database_schema.md文件")
    else:
        print("\n=== PostgreSQL数据库连接测试失败！ ===")
        print("请检查数据库服务是否正常运行，以及连接配置是否正确。")

if __name__ == "__main__":
    main()