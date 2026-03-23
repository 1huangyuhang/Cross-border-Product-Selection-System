# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from algorithm import get_database_tables, get_table_details, get_temu_related_tables

# 创建Flask应用实例
app = Flask(__name__)

# 配置CORS，允许所有来源的请求
CORS(app)

# 添加根路由来提供index.html文件
@app.route('/')
def serve_index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

# 获取所有数据库表的API端点
@app.route('/api/tables', methods=['GET'])
def get_tables():
    tables = get_database_tables()
    return jsonify({'tables': tables})

# 获取所有TEMU相关表的API端点
@app.route('/api/temu-tables', methods=['GET'])
def get_temu_tables():
    tables = get_temu_related_tables()
    return jsonify({'tables': tables})

# 获取指定表的详细信息和数据的API端点
@app.route('/api/table-data/<table_name>', methods=['GET'])
def get_table_data(table_name):
    table_details = get_table_details(table_name)
    return jsonify(table_details)

if __name__ == '__main__':
    # 启动服务，允许外部访问（debug=True仅用于开发）
    # 端口从5001改为5002，因为5001端口也被占用
    app.run(host='0.0.0.0', port=5002, debug=True)