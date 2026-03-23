#!/usr/bin/env python3
"""
数据库API服务
提供数据库表查询和操作接口
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
from datetime import datetime

# 添加算法模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '算法实现最小可行方案'))

try:
    from algorithm import get_database_tables, get_table_details, get_temu_related_tables
except ImportError as e:
    print(f"导入算法模块失败: {e}")
    # 提供备用函数
    def get_database_tables():
        return []
    
    def get_table_details(table_name):
        return {'columns': [], 'data': []}
    
    def get_temu_related_tables():
        return []

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/temu-tables', methods=['GET'])
def get_tables():
    """获取TEMU相关表列表"""
    try:
        tables = get_temu_related_tables()
        return jsonify({
            'success': True,
            'tables': tables,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取表列表失败: {str(e)}',
            'tables': []
        }), 500

@app.route('/api/table-data/<table_name>', methods=['GET'])
def get_table_data(table_name):
    """获取指定表的数据"""
    try:
        table_data = get_table_details(table_name)
        return jsonify({
            'success': True,
            'data': table_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取表数据失败: {str(e)}',
            'data': {'columns': [], 'data': []}
        }), 500

@app.route('/api/all-tables', methods=['GET'])
def get_all_tables():
    """获取所有表列表"""
    try:
        tables = get_database_tables()
        return jsonify({
            'success': True,
            'tables': tables,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取所有表失败: {str(e)}',
            'tables': []
        }), 500

if __name__ == '__main__':
    print("🚀 启动数据库API服务...")
    print("📊 数据库API服务运行在: http://localhost:5002")
    print("🔗 可用接口:")
    print("   - GET /api/health - 健康检查")
    print("   - GET /api/temu-tables - 获取TEMU相关表")
    print("   - GET /api/table-data/<table_name> - 获取表数据")
    print("   - GET /api/all-tables - 获取所有表")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
