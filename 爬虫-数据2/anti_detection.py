#!/usr/bin/env python3
"""
TEMU爬虫反检测模块
提供高级反爬虫检测和处理功能
"""
import time
import random
import json
from typing import Dict, List, Tuple, Optional
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import config
from logger import get_logger

class AntiDetectionHandler:
    """反检测处理器"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = get_logger("AntiDetection")
        self.retry_count = 0
        self.max_retries = config.ANTI_DETECTION_CONFIG["max_retry_attempts"]
    
    def detect_security_verification(self) -> Tuple[bool, str]:
        """检测安全验证页面"""
        try:
            page_title = self.driver.title.lower()
            current_url = self.driver.current_url.lower()
            
            # 检查页面标题中的安全验证关键词
            security_keywords = ['安全验证', 'security', 'verification', 'captcha', '验证']
            for keyword in security_keywords:
                if keyword in page_title:
                    self.logger.info(f"检测到安全验证页面 - 页面标题: {page_title}")
                    return True, f"页面标题包含安全验证关键词: {keyword}"
            
            # 检查URL中的安全验证关键词
            for keyword in security_keywords:
                if keyword in current_url:
                    self.logger.info(f"检测到安全验证页面 - URL: {current_url}")
                    return True, f"URL包含安全验证关键词: {keyword}"
            
            return False, "未检测到安全验证页面"
            
        except Exception as e:
            self.logger.error(f"安全验证检测出错: {e}")
            return False, f"检测过程出错: {e}"
    
    def detect_anti_bot(self) -> Tuple[bool, str]:
        """检测反爬虫系统"""
        try:
            page_source = self.driver.page_source.lower()
            page_title = self.driver.title.lower()
            current_url = self.driver.current_url.lower()
            
            # 检查页面标题
            for indicator in config.ANTI_BOT_INDICATORS:
                if indicator in page_title:
                    self.logger.warning(f"检测到反爬系统 - 页面标题: {page_title}")
                    return True, f"页面标题包含反爬关键词: {indicator}"
            
            # 检查页面内容
            for indicator in config.ANTI_BOT_INDICATORS:
                if indicator in page_source:
                    self.logger.warning(f"检测到反爬系统 - 页面内容: {indicator}")
                    return True, f"页面内容包含反爬关键词: {indicator}"
            
            # 检查URL中的反爬关键词
            for indicator in config.ANTI_BOT_INDICATORS:
                if indicator in current_url:
                    self.logger.warning(f"检测到反爬系统 - URL: {current_url}")
                    return True, f"URL包含反爬关键词: {indicator}"
            
            # 检查是否被重定向到错误页面
            error_pages = ['error', 'blocked', 'forbidden', 'denied', 'access_denied', 'rate_limit']
            for error_page in error_pages:
                if error_page in current_url:
                    self.logger.warning(f"检测到错误页面重定向: {current_url}")
                    return True, f"重定向到错误页面: {current_url}"
            
            # 检查页面是否正常加载（检查是否有商品元素）
            try:
                # 等待页面加载
                time.sleep(2)
                
                # 检查是否有商品元素
                has_products = False
                for selector in config.PRODUCT_SELECTORS:
                    try:
                        elements = self.driver.find_elements("css selector", selector)
                        if elements and len(elements) > 0:
                            has_products = True
                            break
                    except:
                        continue
                
                if not has_products:
                    # 检查是否有搜索框（说明页面正常但可能没有商品）
                    has_search = False
                    for selector in config.SEARCH_SELECTORS:
                        try:
                            elements = self.driver.find_elements("css selector", selector)
                            if elements and len(elements) > 0:
                                has_search = True
                                break
                        except:
                            continue
                    
                    if not has_search:
                        self.logger.warning("页面中未找到商品或搜索元素，可能被反爬系统阻止")
                        return True, "页面中未找到商品或搜索元素"
                
            except Exception as e:
                self.logger.debug(f"检查页面元素时出错: {e}")
            
            return False, "未检测到反爬系统"
            
        except Exception as e:
            self.logger.error(f"反爬检测出错: {e}")
            return False, f"检测过程出错: {e}"
    
    def wait_for_manual_verification(self) -> bool:
        """等待用户手动完成安全验证"""
        try:
            self.logger.info("🔐 检测到安全验证页面，等待用户手动完成验证...")
            print("\n" + "="*60)
            print("🔐 安全验证检测")
            print("="*60)
            print("⚠️  检测到安全验证页面，请手动完成验证")
            print("💡 请在浏览器中完成以下操作：")
            print("   1. 完成滑块验证（如果有）")
            print("   2. 点击验证按钮")
            print("   3. 等待页面跳转到正常页面")
            print("⏰ 程序将等待您完成验证，最多等待5分钟...")
            print("="*60)
            
            # 等待用户手动完成验证，最多5分钟
            max_wait_time = 300  # 5分钟
            check_interval = 5   # 每5秒检查一次
            
            for i in range(0, max_wait_time, check_interval):
                time.sleep(check_interval)
                
                # 检查是否还在安全验证页面
                is_verification, message = self.detect_security_verification()
                if not is_verification:
                    self.logger.info("✅ 安全验证已完成，页面已跳转")
                    print("\n✅ 检测到安全验证已完成，继续爬取...")
                    return True
                
                # 显示等待进度
                remaining_time = max_wait_time - i
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                
                if i % 30 == 0:  # 每30秒显示一次进度
                    print(f"⏳ 等待验证完成... 剩余时间: {minutes}分{seconds}秒")
                    self.logger.info(f"等待安全验证完成... 剩余时间: {remaining_time}秒")
            
            # 超时处理
            self.logger.warning("安全验证等待超时")
            print("\n⏰ 等待超时，请检查是否已完成安全验证")
            
            # 最后检查一次
            is_verification, _ = self.detect_security_verification()
            if not is_verification:
                self.logger.info("✅ 最终检查：安全验证已完成")
                print("✅ 检测到安全验证已完成，继续爬取...")
                return True
            else:
                self.logger.error("❌ 安全验证未完成，程序终止")
                print("❌ 安全验证未完成，程序终止")
                return False
            
        except Exception as e:
            self.logger.error(f"等待安全验证时出错: {e}")
            print(f"❌ 等待安全验证时出错: {e}")
            return False
    
    def handle_anti_bot(self) -> bool:
        """处理反爬虫系统"""
        try:
            self.logger.info("🛡️ 开始处理反爬系统...")
            self.retry_count += 1
            
            if self.retry_count > self.max_retries:
                self.logger.error(f"已达到最大重试次数: {self.max_retries}")
                return False
            
            print(f"\n🛡️ 反爬系统处理 - 第 {self.retry_count} 次尝试")
            print("="*50)
            
            # 策略1: 等待冷却期
            wait_time = random.uniform(15, 30) * self.retry_count
            print(f"⏳ 策略1: 等待冷却期 {wait_time:.1f}秒...")
            time.sleep(wait_time)
            
            # 策略2: 清除浏览器数据
            print("🧹 策略2: 清除浏览器数据...")
            self._clear_browser_data()
            
            # 策略3: 更换User-Agent
            print("🔄 策略3: 更换User-Agent...")
            self._change_user_agent()
            
            # 策略4: 模拟人类行为
            print("🤖 策略4: 模拟人类行为...")
            self._simulate_human_behavior()
            
            # 策略5: 刷新页面
            print("🔄 策略5: 刷新页面...")
            try:
                self.driver.refresh()
                time.sleep(5)
            except:
                pass
            
            # 策略6: 重新导航到首页
            print("🌐 策略6: 重新导航到首页...")
            try:
                self.driver.get("https://www.temu.com")
                time.sleep(5)
            except:
                pass
            
            # 策略7: 使用代理（如果配置了）
            if config.PROXY_CONFIG["enabled"]:
                print("🌐 策略7: 更换代理...")
                self._change_proxy()
            
            # 重新检查
            print("🔍 检查反爬系统状态...")
            time.sleep(3)
            is_anti_bot, message = self.detect_anti_bot()
            
            if not is_anti_bot:
                print("✅ 反爬系统处理成功")
                self.logger.info("反爬系统处理成功")
                self.retry_count = 0
                return True
            else:
                print(f"⚠️ 反爬系统仍然存在: {message}")
                self.logger.warning(f"反爬系统仍然存在: {message}")
                if self.retry_count < self.max_retries:
                    print(f"🔄 准备第 {self.retry_count + 1} 次重试...")
                    self.logger.info(f"准备第 {self.retry_count + 1} 次重试...")
                    return self.handle_anti_bot()
                else:
                    print("❌ 无法解决反爬系统")
                    self.logger.error("无法解决反爬系统")
                    return False
                    
        except Exception as e:
            print(f"❌ 反爬系统处理出错: {e}")
            self.logger.error(f"反爬系统处理出错: {e}")
            return False
    
    def _clear_browser_data(self):
        """清除浏览器数据"""
        try:
            # 清除cookies
            self.driver.delete_all_cookies()
            
            # 清除本地存储
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.execute_script("window.sessionStorage.clear();")
            
            # 清除缓存
            self.driver.execute_script("window.caches.keys().then(names => names.forEach(name => window.caches.delete(name)));")
            
            self.logger.debug("浏览器数据清除完成")
            
        except Exception as e:
            self.logger.warning(f"清除浏览器数据时出错: {e}")
    
    def _change_user_agent(self):
        """更换User-Agent"""
        try:
            new_ua = config.get_user_agent()
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": new_ua})
            self.logger.debug(f"User-Agent已更换: {new_ua[:50]}...")
            
        except Exception as e:
            self.logger.warning(f"更换User-Agent时出错: {e}")
    
    def _simulate_human_behavior(self):
        """模拟人类行为"""
        try:
            print("🤖 开始模拟人类行为...")
            
            # 1. 模拟阅读行为 - 缓慢滚动
            print("📖 模拟阅读行为...")
            for _ in range(random.randint(2, 4)):
                scroll_y = random.randint(100, 300)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_y});")
                time.sleep(random.uniform(2, 4))
            
            # 2. 模拟鼠标移动
            print("🖱️ 模拟鼠标移动...")
            try:
                actions = ActionChains(self.driver)
                for _ in range(random.randint(3, 6)):
                    x = random.randint(200, 1000)
                    y = random.randint(200, 600)
                    actions.move_by_offset(x, y).perform()
                    time.sleep(random.uniform(0.8, 1.5))
            except:
                pass
            
            # 3. 模拟点击行为
            print("👆 模拟点击行为...")
            try:
                # 尝试点击一些安全元素
                safe_selectors = ['body', 'main', 'div[class*="container"]', 'header', 'nav']
                for selector in safe_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            element = random.choice(elements)
                            if element.is_displayed():
                                actions = ActionChains(self.driver)
                                actions.move_to_element(element).click().perform()
                                time.sleep(random.uniform(1, 2))
                                break
                    except:
                        continue
            except:
                pass
            
            # 4. 模拟键盘行为
            print("⌨️ 模拟键盘行为...")
            try:
                from selenium.webdriver.common.keys import Keys
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.TAB).perform()
                time.sleep(random.uniform(0.5, 1))
                actions.send_keys(Keys.TAB).perform()
                time.sleep(random.uniform(0.5, 1))
            except:
                pass
            
            # 5. 模拟浏览行为 - 查看不同区域
            print("👀 模拟浏览行为...")
            try:
                # 滚动到顶部
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(random.uniform(1, 2))
                
                # 滚动到中间
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(random.uniform(1, 2))
                
                # 滚动到底部
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 2))
            except:
                pass
            
            print("✅ 人类行为模拟完成")
            
        except Exception as e:
            print(f"⚠️ 模拟人类行为时出错: {e}")
            self.logger.warning(f"模拟人类行为时出错: {e}")
    
    def _change_proxy(self):
        """更换代理"""
        try:
            if config.PROXY_CONFIG["proxies"]:
                proxy = random.choice(config.PROXY_CONFIG["proxies"])
                # 这里需要重新创建driver实例来应用新代理
                self.logger.debug(f"尝试更换代理: {proxy}")
            else:
                self.logger.warning("未配置代理列表")
                
        except Exception as e:
            self.logger.warning(f"更换代理时出错: {e}")
    
    def comprehensive_check(self) -> Tuple[bool, str]:
        """综合检查页面状态"""
        try:
            # 检查安全验证页面
            is_verification, verification_msg = self.detect_security_verification()
            if is_verification:
                return False, f"检测到安全验证页面: {verification_msg}"
            
            # 检查反爬系统
            is_anti_bot, anti_bot_msg = self.detect_anti_bot()
            if is_anti_bot:
                return False, f"检测到反爬系统: {anti_bot_msg}"
            
            # 检查页面是否正常加载
            try:
                page_title = self.driver.title
                if not page_title or len(page_title.strip()) < 3:
                    return False, "页面标题异常"
            except:
                return False, "无法获取页面标题"
            
            # 检查是否有商品元素
            has_products = False
            for selector in config.PRODUCT_SELECTORS:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and len(elements) > 0:
                        has_products = True
                        break
                except:
                    continue
            
            if not has_products:
                return False, "页面中未找到商品元素"
            
            return True, "页面状态正常"
            
        except Exception as e:
            self.logger.error(f"综合检查出错: {e}")
            return False, f"检查过程出错: {e}"
