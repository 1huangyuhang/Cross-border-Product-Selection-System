#!/usr/bin/env python3
"""
跨境电商选品系统 - 数据库迁移工具
按照software.md文档要求实现数据库迁移
"""

import os
import psycopg2
from sqlalchemy import create_engine, text
import logging
from typing import List, Tuple
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseMigrator:
    """数据库迁移工具 - 按照software.md文档要求实现"""
    
    def __init__(self, connection_string: str = None):
        """
        初始化迁移工具
        按照software.md文档要求使用PostgreSQL
        """
        self.connection_string = connection_string or \
            "postgresql://postgres:password@localhost:5432/ecommerce_db"
        
        try:
            self.engine = create_engine(self.connection_string)
            logger.info("数据库迁移工具初始化成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            raise
    
    def run_migrations(self, migrations_dir: str = "migrations") -> bool:
        """
        运行所有待执行的迁移
        按照software.md文档要求实现迁移执行
        """
        try:
            # 确保迁移记录表存在
            self._ensure_migrations_table()
            
            # 获取已应用的迁移
            applied_migrations = self._get_applied_migrations()
            
            # 获取所有迁移文件
            migration_files = self._get_migration_files(migrations_dir)
            
            # 执行待执行的迁移
            for migration_file in migration_files:
                version = self._extract_version_from_filename(migration_file)
                
                if version not in applied_migrations:
                    logger.info(f"执行迁移: {migration_file}")
                    if self._run_migration(migration_file, version):
                        logger.info(f"迁移 {version} 执行成功")
                    else:
                        logger.error(f"迁移 {version} 执行失败")
                        return False
                else:
                    logger.info(f"迁移 {version} 已应用，跳过")
            
            logger.info("所有迁移执行完成")
            return True
            
        except Exception as e:
            logger.error(f"迁移执行失败: {str(e)}")
            return False
    
    def _ensure_migrations_table(self):
        """确保迁移记录表存在"""
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(255) PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                description TEXT
            )
        """
        
        with self.engine.connect() as conn:
            conn.execute(text(create_table_sql))
            conn.commit()
    
    def _get_applied_migrations(self) -> List[str]:
        """获取已应用的迁移版本"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT version FROM schema_migrations ORDER BY version"))
                return [row[0] for row in result]
        except Exception as e:
            logger.error(f"获取已应用迁移失败: {str(e)}")
            return []
    
    def _get_migration_files(self, migrations_dir: str) -> List[str]:
        """获取所有迁移文件"""
        migration_files = []
        
        if not os.path.exists(migrations_dir):
            logger.warning(f"迁移目录不存在: {migrations_dir}")
            return migration_files
        
        for filename in sorted(os.listdir(migrations_dir)):
            if filename.endswith('.sql'):
                migration_files.append(os.path.join(migrations_dir, filename))
        
        return migration_files
    
    def _extract_version_from_filename(self, filename: str) -> str:
        """从文件名提取版本号"""
        basename = os.path.basename(filename)
        return basename.split('_')[0]
    
    def _run_migration(self, migration_file: str, version: str) -> bool:
        """执行单个迁移文件"""
        try:
            with open(migration_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            with self.engine.connect() as conn:
                # 执行迁移SQL
                conn.execute(text(sql_content))
                conn.commit()
            
            logger.info(f"迁移 {version} 执行成功")
            return True
            
        except Exception as e:
            logger.error(f"迁移 {version} 执行失败: {str(e)}")
            return False
    
    def rollback_migration(self, version: str) -> bool:
        """回滚指定版本的迁移"""
        try:
            # 这里需要根据实际情况实现回滚逻辑
            # 由于SQL迁移文件通常不包含回滚信息，这里只是示例
            logger.warning(f"回滚迁移 {version} - 需要手动实现回滚逻辑")
            return False
            
        except Exception as e:
            logger.error(f"回滚迁移 {version} 失败: {str(e)}")
            return False
    
    def get_migration_status(self) -> List[Tuple[str, str, str]]:
        """获取迁移状态"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT version, applied_at, description 
                    FROM schema_migrations 
                    ORDER BY version
                """))
                
                return [(row[0], str(row[1]), row[2] or '') for row in result]
                
        except Exception as e:
            logger.error(f"获取迁移状态失败: {str(e)}")
            return []

def main():
    """主函数"""
    logger.info("开始数据库迁移...")
    
    migrator = DatabaseMigrator()
    
    if migrator.run_migrations():
        logger.info("数据库迁移完成")
        
        # 显示迁移状态
        status = migrator.get_migration_status()
        if status:
            logger.info("迁移状态:")
            for version, applied_at, description in status:
                logger.info(f"  {version}: {applied_at} - {description}")
    else:
        logger.error("数据库迁移失败")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
