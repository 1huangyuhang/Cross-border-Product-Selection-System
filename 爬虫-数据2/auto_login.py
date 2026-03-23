#!/usr/bin/env python3
"""
TEMU自动登录模块
保存登录状态，实现自动登录功能
"""
import os
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import config
from logger import get_logger

class AutoLogin:
    """自动登录处理器"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger("AutoLogin")
        self.login_file = "data/login_info.json"
        self.cookies_file = "data/temu_cookies.json"
        
        # 确保数据目录存在
        os.makedirs("data", exist_ok=True)
    
    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        try:
            # 检查URL是否包含登录相关路径
            current_url = self.driver.current_url.lower()
            if any(path in current_url for path in ['login', 'signin', 'auth']):
                return False
            
            # 检查页面是否有登录按钮（说明未登录）
            login_selectors = [
                'a[href*="login"]',
                'button[class*="login"]',
                '[data-testid*="login"]',
                '.login-btn',
                '#login'
            ]
            
            for selector in login_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    if elements and any(elem.is_displayed() for elem in elements):
                        self.logger.info("检测到登录按钮，用户未登录")
                        return False
                except:
                    continue
            
            # 检查是否有用户头像或用户名（说明已登录）
            user_selectors = [
                '[class*="avatar"]',
                '[class*="user"]',
                '[class*="profile"]',
                '.user-info',
                '.account'
            ]
            
            for selector in user_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    if elements and any(elem.is_displayed() for elem in elements):
                        self.logger.info("检测到用户信息，用户已登录")
                        return True
                except:
                    continue
            
            # 检查页面标题
            page_title = self.driver.title.lower()
            if 'login' in page_title or 'sign in' in page_title:
                return False
            
            # 默认认为已登录（如果页面正常加载）
            return True
            
        except Exception as e:
            self.logger.error(f"检查登录状态时出错: {e}")
            return False
    
    def save_login_info(self, login_data: Dict):
        """保存登录信息"""
        try:
            login_data['saved_at'] = datetime.now().isoformat()
            login_data['expires_at'] = (datetime.now() + timedelta(days=7)).isoformat()
            
            with open(self.login_file, 'w', encoding='utf-8') as f:
                json.dump(login_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info("登录信息已保存")
            
        except Exception as e:
            self.logger.error(f"保存登录信息失败: {e}")
    
    def load_login_info(self) -> Optional[Dict]:
        """加载登录信息"""
        try:
            if not os.path.exists(self.login_file):
                return None
            
            with open(self.login_file, 'r', encoding='utf-8') as f:
                login_data = json.load(f)
            
            # 检查是否过期
            expires_at = datetime.fromisoformat(login_data.get('expires_at', ''))
            if datetime.now() > expires_at:
                self.logger.info("登录信息已过期")
                return None
            
            self.logger.info("登录信息加载成功")
            return login_data
            
        except Exception as e:
            self.logger.error(f"加载登录信息失败: {e}")
            return None
    
    def save_cookies(self):
        """保存浏览器cookies"""
        try:
            cookies = self.driver.get_cookies()
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            self.logger.info("Cookies已保存")
            
        except Exception as e:
            self.logger.error(f"保存Cookies失败: {e}")
    
    def load_cookies(self) -> bool:
        """加载浏览器cookies"""
        try:
            if not os.path.exists(self.cookies_file):
                return False
            
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            # 先导航到TEMU域名
            self.driver.get("https://www.temu.com")
            time.sleep(2)
            
            # 添加cookies
            for cookie in cookies:
                try:
                    # 移除domain前的点
                    if cookie.get('domain', '').startswith('.'):
                        cookie['domain'] = cookie['domain'][1:]
                    
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    self.logger.debug(f"添加cookie失败: {e}")
                    continue
            
            # 刷新页面使cookies生效
            self.driver.refresh()
            time.sleep(3)
            
            self.logger.info("Cookies已加载")
            return True
            
        except Exception as e:
            self.logger.error(f"加载Cookies失败: {e}")
            return False
    
    def auto_login(self) -> bool:
        """自动登录"""
        try:
            print("\n🔐 检查登录状态...")
            
            # 首先尝试加载cookies
            if self.load_cookies():
                print("🍪 尝试使用保存的Cookies登录...")
                time.sleep(3)
                
                if self.is_logged_in():
                    print("✅ 使用Cookies自动登录成功")
                    return True
                else:
                    print("⚠️ Cookies登录失败，需要手动登录")
            
            # 如果cookies登录失败，提示用户手动登录
            print("\n" + "="*60)
            print("🔐 需要手动登录")
            print("="*60)
            print("💡 请在浏览器中完成以下操作：")
            print("   1. 输入用户名/邮箱")
            print("   2. 输入密码")
            print("   3. 完成验证码（如果有）")
            print("   4. 点击登录按钮")
            print("   5. 等待页面跳转到首页")
            print("⏰ 程序将等待您完成登录，最多等待5分钟...")
            print("="*60)
            
            # 等待用户手动登录
            max_wait_time = 300  # 5分钟
            check_interval = 5   # 每5秒检查一次
            
            for i in range(0, max_wait_time, check_interval):
                time.sleep(check_interval)
                
                if self.is_logged_in():
                    print("\n✅ 检测到登录成功")
                    
                    # 保存登录状态
                    self.save_cookies()
                    self.save_login_info({
                        'login_time': datetime.now().isoformat(),
                        'status': 'success'
                    })
                    
                    return True
                
                # 显示等待进度
                remaining_time = max_wait_time - i
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                
                if i % 30 == 0:  # 每30秒显示一次进度
                    print(f"⏳ 等待登录完成... 剩余时间: {minutes}分{seconds}秒")
            
            # 超时处理
            print("\n⏰ 登录等待超时")
            return False
            
        except Exception as e:
            self.logger.error(f"自动登录失败: {e}")
            print(f"❌ 自动登录失败: {e}")
            return False
    
    def ensure_logged_in(self) -> bool:
        """确保用户已登录"""
        try:
            # 检查当前登录状态
            if self.is_logged_in():
                print("✅ 用户已登录")
                return True
            
            # 尝试自动登录
            return self.auto_login()
            
        except Exception as e:
            self.logger.error(f"确保登录状态失败: {e}")
            return False
