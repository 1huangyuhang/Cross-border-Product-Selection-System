#!/usr/bin/env python3
"""
启动数据分析系统
同时启动数据库API和分析API服务
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path

def start_service(script_path, port, service_name):
    """启动服务"""
    try:
        print(f"🚀 启动 {service_name} 服务 (端口: {port})...")
        process = subprocess.Popen([
            sys.executable, script_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 等待服务启动
        time.sleep(3)
        
        if process.poll() is None:
            print(f"✅ {service_name} 服务启动成功")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ {service_name} 服务启动失败")
            print(f"错误输出: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 启动 {service_name} 服务时出错: {e}")
        return None

def main():
    """主函数"""
    print("🕷️ TEMU跨境电商选品数据分析系统")
    print("="*60)
    
    # 获取当前目录
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    # 服务配置
    services = [
        {
            'script': current_dir / 'app.py',
            'port': 5002,
            'name': '数据库API服务'
        },
        {
            'script': current_dir / 'analysis_api.py',
            'port': 5003,
            'name': '数据分析API服务'
        }
    ]
    
    processes = []
    
    try:
        # 启动所有服务
        for service in services:
            if service['script'].exists():
                process = start_service(
                    str(service['script']), 
                    service['port'], 
                    service['name']
                )
                if process:
                    processes.append(process)
            else:
                print(f"⚠️ 服务脚本不存在: {service['script']}")
        
        if not processes:
            print("❌ 没有成功启动任何服务")
            return
        
        print("\n" + "="*60)
        print("🎉 数据分析系统启动完成！")
        print("="*60)
        print("📊 服务地址:")
        print("   - 数据库API: http://localhost:5002")
        print("   - 数据分析API: http://localhost:5003")
        print("   - 前端界面: 打开 index.html 文件")
        print("\n💡 使用说明:")
        print("   1. 在浏览器中打开 index.html")
        print("   2. 选择数据库表或加载示例数据")
        print("   3. 点击'开始数据分析'按钮")
        print("   4. 查看分析结果和图表")
        print("\n⏹️ 按 Ctrl+C 停止所有服务")
        print("="*60)
        
        # 等待用户中断
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n🛑 正在停止所有服务...")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 正在停止所有服务...")
    finally:
        # 停止所有服务
        for process in processes:
            if process and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("✅ 所有服务已停止")

if __name__ == '__main__':
    main()
