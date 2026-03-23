#!/usr/bin/env python3
"""
TEMU爬虫系统 - 直接运行版本
简化版，直接开始爬取，无需交互
"""
import os
import sys
import time
import json
import random
from datetime import datetime
from selenium.webdriver.common.keys import Keys

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawlers'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))

from config import config
from logger import get_logger
from anti_detection import AntiDetectionHandler
from auto_login import AutoLogin

class SimpleTemuCrawler:
    """简化版TEMU爬虫"""
    
    def __init__(self, keyword="手机配件", max_pages=2, email="", password=""):
        self.keyword = keyword
        self.max_pages = max_pages
        self.driver = None
        self.logger = get_logger("SimpleCrawler")
        self.email = email
        self.password = password
        
        # 确保目录存在
        config.ensure_directories()
    
    def setup_driver(self) -> bool:
        """设置浏览器驱动"""
        try:
            print("🚀 启动TEMU爬虫系统...")
            print(f"🔍 搜索关键词: {self.keyword}")
            print(f"📄 爬取页数: {self.max_pages}")
            print("="*50)
            
            # 使用普通Selenium WebDriver
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.chrome.options import Options
            from webdriver_manager.chrome import ChromeDriverManager
            
            # 设置Chrome选项 - 增强反检测
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # 设置随机窗口大小
            import random
            width = random.randint(1200, 1920)
            height = random.randint(800, 1080)
            options.add_argument(f"--window-size={width},{height}")
            
            # 设置更真实的用户代理
            user_agents = [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ]
            options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # 执行反检测脚本
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            self.driver.set_page_load_timeout(30)
            
            # 初始化反检测处理器
            self.anti_detection = AntiDetectionHandler(self.driver)
            
            # 初始化自动登录处理器
            self.auto_login = AutoLogin(self.driver)
            
            print("✅ 浏览器驱动设置成功")
            return True
            
        except Exception as e:
            print(f"❌ 浏览器驱动设置失败: {e}")
            return False
    
    def navigate_to_temu(self) -> bool:
        """导航到TEMU首页"""
        try:
            print("🌐 导航到TEMU首页...")
            self.driver.get("https://www.temu.com")
            time.sleep(5)
            
            # 检查页面状态
            is_valid, message = self.anti_detection.comprehensive_check()
            if is_valid:
                print(f"✅ 页面导航成功: {message}")
                
                # 检查是否需要登录
                if self._check_login_required():
                    print("🔐 检测到登录页面，开始自动登录...")
                    if self._auto_login():
                        print("✅ 自动登录成功")
                        return True
                    else:
                        print("❌ 自动登录失败")
                        return False
                else:
                    print("✅ 无需登录，直接继续")
                    return True
            else:
                print(f"⚠️ 页面状态异常: {message}")
                return self._handle_page_issues()
                
        except Exception as e:
            print(f"❌ 导航到TEMU失败: {e}")
            return False
    
    def _handle_page_issues(self) -> bool:
        """处理页面问题"""
        try:
            # 检查安全验证页面
            is_verification, verification_msg = self.anti_detection.detect_security_verification()
            if is_verification:
                print(f"🔐 检测到安全验证页面: {verification_msg}")
                if self.anti_detection.wait_for_manual_verification():
                    print("✅ 安全验证已完成，继续爬取")
                    return True
                else:
                    print("❌ 安全验证未完成，程序终止")
                    return False
            
            return False
            
        except Exception as e:
            print(f"❌ 处理页面问题时出错: {e}")
            return False
    
    def _check_login_required(self) -> bool:
        """检查是否需要登录"""
        try:
            current_url = self.driver.current_url.lower()
            page_title = self.driver.title.lower()
            
            # 检查URL是否包含登录相关路径
            if any(path in current_url for path in ['login', 'signin', 'auth']):
                print("🔍 检测到登录URL")
                return True
            
            # 检查页面标题
            if any(keyword in page_title for keyword in ['login', 'sign in', '登录']):
                print("🔍 检测到登录页面标题")
                return True
            
            # 检查是否有登录表单
            login_selectors = [
                'input[type="email"]',
                'input[type="text"][aria-label*="邮件"]',
                'input[type="text"][aria-label*="电话"]',
                'input[placeholder*="email"]',
                'input[placeholder*="phone"]',
                'input[name="email"]',
                'input[name="phone"]'
            ]
            
            for selector in login_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    if elements and any(elem.is_displayed() for elem in elements):
                        print(f"🔍 检测到登录表单: {selector}")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"⚠️ 检查登录状态时出错: {e}")
            return False
    
    def _auto_login(self) -> bool:
        """手动登录等待模式"""
        try:
            print("\n" + "="*60)
            print("🔐 手动登录模式")
            print("="*60)
            print("💡 请在浏览器中完成登录：")
            print("   1. 使用Google登录或其他方式登录")
            print("   2. 完成所有验证步骤")
            print("   3. 等待跳转到TEMU首页")
            print("⏰ 程序将等待您完成登录，最多等待5分钟...")
            print("="*60)
            
            # 等待用户手动登录
            max_wait_time = 300  # 5分钟
            check_interval = 5   # 每5秒检查一次
            
            for i in range(0, max_wait_time, check_interval):
                time.sleep(check_interval)
                
                if self._check_login_success():
                    print("\n✅ 手动登录成功")
                    return True
                
                # 显示等待进度
                remaining_time = max_wait_time - i
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                
                if i % 30 == 0:  # 每30秒显示一次进度
                    print(f"⏳ 等待登录完成... 剩余时间: {minutes}分{seconds}秒")
            
            print("\n⏰ 登录等待超时")
            return False
            
        except Exception as e:
            print(f"❌ 手动登录处理出错: {e}")
            return False
    
    
    def _check_login_success(self) -> bool:
        """检查登录是否成功"""
        try:
            # 等待页面跳转
            time.sleep(3)
            
            # 检查URL是否跳转到首页
            current_url = self.driver.current_url.lower()
            if 'login' not in current_url and 'signin' not in current_url:
                return True
            
            # 检查是否有用户信息显示
            user_selectors = [
                '[class*="user"]',
                '[class*="profile"]',
                '[class*="avatar"]',
                '.user-info',
                '.account'
            ]
            
            for selector in user_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    if elements and any(elem.is_displayed() for elem in elements):
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"⚠️ 检查登录状态时出错: {e}")
            return False
    
    
    def search_products(self) -> bool:
        """搜索商品"""
        try:
            print(f"🔍 开始搜索商品: {self.keyword}")
            
            # 查找搜索框
            search_input = self._find_search_box()
            if not search_input:
                print("❌ 未找到搜索框")
                return False
            
            # 输入搜索关键词
            print("⌨️ 输入搜索关键词...")
            search_input.clear()
            time.sleep(0.5)
            search_input.send_keys(self.keyword)
            time.sleep(1)
            
            # 执行搜索
            print("🚀 执行搜索...")
            search_input.send_keys(Keys.RETURN)
            time.sleep(3)
            
            # 检查搜索结果
            is_valid, message = self.anti_detection.comprehensive_check()
            if is_valid:
                print(f"✅ 搜索成功: {message}")
                return True
            else:
                print(f"⚠️ 搜索结果异常: {message}")
                
                # 检查是否是反爬系统
                is_anti_bot, anti_bot_msg = self.anti_detection.detect_anti_bot()
                if is_anti_bot:
                    print(f"🛡️ 检测到反爬系统: {anti_bot_msg}")
                    if self.anti_detection.handle_anti_bot():
                        print("✅ 反爬系统处理成功，继续搜索")
                        return True
                    else:
                        print("❌ 无法处理反爬系统")
                        return False
                
                return False
                
        except Exception as e:
            print(f"❌ 搜索商品失败: {e}")
            return False
    
    def _find_search_box(self):
        """查找搜索框"""
        for selector in config.SEARCH_SELECTORS:
            try:
                elements = self.driver.find_elements("css selector", selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        print(f"✅ 找到搜索框: {selector}")
                        return element
            except:
                continue
        
        print("❌ 未找到可用的搜索框")
        return None
    
    
    
    def crawl_products(self) -> list:
        """爬取商品信息"""
        products = []
        
        try:
            print(f"\n📦 开始爬取商品...")
            
            # 设置驱动
            if not self.setup_driver():
                return products
            
            # 导航到TEMU
            if not self._safe_navigate_to_temu():
                return products
            
            # 搜索商品
            if not self._safe_search_products():
                return products
            
            # 爬取商品
            for page in range(1, self.max_pages + 1):
                print(f"\n📄 开始爬取第 {page} 页...")
                
                page_products = self._safe_crawl_page(page)
                if page_products:
                    products.extend(page_products)
                    print(f"✅ 第 {page} 页获取 {len(page_products)} 个商品")
                else:
                    print(f"⚠️ 第 {page} 页未找到商品")
                
                # 尝试翻页
                if page < self.max_pages:
                    if not self._safe_go_to_next_page():
                        print("ℹ️ 无法翻页，可能已到最后一页")
                        break
            
            return products
            
        except Exception as e:
            print(f"❌ 爬取过程出错: {e}")
            return products
        
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                    print("🔚 浏览器已关闭")
                except:
                    print("🔚 浏览器已关闭（强制）")
    
    def _check_driver_alive(self) -> bool:
        """检查驱动是否还活着"""
        try:
            if not self.driver:
                return False
            # 尝试获取当前URL
            self.driver.current_url
            return True
        except:
            return False
    
    def _safe_navigate_to_temu(self) -> bool:
        """安全的导航到TEMU"""
        try:
            if not self._check_driver_alive():
                print("❌ 浏览器窗口已关闭，无法继续")
                return False
            return self.navigate_to_temu()
        except Exception as e:
            print(f"❌ 安全导航失败: {e}")
            return False
    
    def _safe_search_products(self) -> bool:
        """安全的搜索商品"""
        try:
            if not self._check_driver_alive():
                print("❌ 浏览器窗口已关闭，无法继续")
                return False
            return self.search_products()
        except Exception as e:
            print(f"❌ 安全搜索失败: {e}")
            return False
    
    def _safe_crawl_page(self, page: int) -> list:
        """安全的爬取单页"""
        try:
            if not self._check_driver_alive():
                print("❌ 浏览器窗口已关闭，无法继续")
                return []
            return self._crawl_page(page)
        except Exception as e:
            print(f"❌ 安全爬取第 {page} 页失败: {e}")
            return []
    
    def _safe_go_to_next_page(self) -> bool:
        """安全的翻页"""
        try:
            if not self._check_driver_alive():
                print("❌ 浏览器窗口已关闭，无法继续")
                return False
            return self._go_to_next_page()
        except Exception as e:
            print(f"❌ 安全翻页失败: {e}")
            return False
    
    def _crawl_page(self, page: int) -> list:
        """爬取单页商品"""
        try:
            # 滚动加载更多商品
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # 查找商品元素
            page_products = []
            for selector in config.PRODUCT_SELECTORS:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    if elements:
                        print(f"🔍 找到 {len(elements)} 个商品元素")
                        
                        for element in elements[:20]:  # 限制每页最多20个商品
                            try:
                                product_info = self._extract_product_info(element)
                                if product_info and product_info.get('title'):
                                    page_products.append(product_info)
                            except Exception as e:
                                continue
                        break
                except Exception as e:
                    continue
            
            return page_products
            
        except Exception as e:
            print(f"❌ 爬取第 {page} 页失败: {e}")
            return []
    
    def _extract_product_info(self, element) -> dict:
        """提取商品信息 - 增强容错逻辑"""
        try:
            product_info = {}
            
            # 提取标题 - 更多选择器
            title_selectors = [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                '.title', '[class*="title"]', '[class*="name"]',
                'a', 'span[class*="title"]', 'div[class*="title"]',
                '[data-testid*="title"]', '[aria-label*="title"]'
            ]
            for selector in title_selectors:
                try:
                    title_elem = element.find_element("css selector", selector)
                    if title_elem and title_elem.text.strip():
                        product_info['title'] = title_elem.text.strip()
                        break
                except:
                    continue
            
            # 提取价格 - 更多选择器
            price_selectors = [
                '.price', '[class*="price"]', '.cost', '[class*="cost"]',
                '.amount', '[class*="amount"]', '.value', '[class*="value"]',
                'span[class*="price"]', 'div[class*="price"]',
                '[data-testid*="price"]', '[aria-label*="price"]',
                'span:contains("$")', 'span:contains("¥")', 'span:contains("€")'
            ]
            for selector in price_selectors:
                try:
                    price_elem = element.find_element("css selector", selector)
                    if price_elem and price_elem.text.strip():
                        product_info['price'] = price_elem.text.strip()
                        break
                except:
                    continue
            
            # 提取链接 - 更多选择器
            link_selectors = ['a', '[href]', '[data-href]']
            for selector in link_selectors:
                try:
                    link_elem = element.find_element("css selector", selector)
                    if link_elem:
                        href = link_elem.get_attribute('href') or link_elem.get_attribute('data-href')
                        if href and ('http' in href or href.startswith('/')):
                            product_info['link'] = href
                            break
                except:
                    continue
            
            # 提取图片
            try:
                img_elem = element.find_element("css selector", "img")
                if img_elem:
                    img_src = img_elem.get_attribute('src') or img_elem.get_attribute('data-src')
                    if img_src:
                        product_info['image'] = img_src
            except:
                pass
            
            # 提取评分
            rating_selectors = [
                '[class*="rating"]', '[class*="score"]', '[class*="star"]',
                '.rating', '.score', '.stars'
            ]
            for selector in rating_selectors:
                try:
                    rating_elem = element.find_element("css selector", selector)
                    if rating_elem and rating_elem.text.strip():
                        product_info['rating'] = rating_elem.text.strip()
                        break
                except:
                    continue
            
            # 提取销量
            sales_selectors = [
                '[class*="sales"]', '[class*="sold"]', '[class*="orders"]',
                '.sales', '.sold', '.orders'
            ]
            for selector in sales_selectors:
                try:
                    sales_elem = element.find_element("css selector", selector)
                    if sales_elem and sales_elem.text.strip():
                        product_info['sales'] = sales_elem.text.strip()
                        break
                except:
                    continue
            
            # 即使部分字段缺失也返回商品信息
            if product_info.get('title') or product_info.get('price') or product_info.get('link'):
                return product_info
            
            return {}
            
        except Exception as e:
            return {}
    
    def _go_to_next_page(self) -> bool:
        """翻到下一页"""
        try:
            next_selectors = [
                'a[aria-label*="下一页"]',
                'a[aria-label*="next"]',
                'button[aria-label*="下一页"]',
                'button[aria-label*="next"]',
                '.next',
                '[class*="next"]'
            ]
            
            for selector in next_selectors:
                try:
                    next_btn = self.driver.find_element("css selector", selector)
                    if next_btn.is_displayed() and next_btn.is_enabled():
                        next_btn.click()
                        time.sleep(3)
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            return False
    
    def save_results(self, products: list):
        """保存结果"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/simple_temu_{self.keyword}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"💾 结果已保存: {filename}")
            
            # 显示商品预览
            self._show_product_preview(products)
            
        except Exception as e:
            print(f"❌ 保存结果失败: {e}")
    
    def _show_product_preview(self, products: list):
        """显示商品预览"""
        try:
            print(f"\n📋 商品预览 (前5个):")
            for i, product in enumerate(products[:5], 1):
                print(f"  {i}. 标题: {product.get('title', 'N/A')[:60]}...")
                print(f"     价格: {product.get('price', 'N/A')}")
                print(f"     链接: {product.get('link', 'N/A')[:50]}...")
                print()
                
        except Exception as e:
            print(f"❌ 显示商品预览失败: {e}")

def main():
    """主函数"""
    print("🕷️ TEMU跨境电商选品爬虫系统")
    print("💻 简化版 - 直接运行")
    print("="*60)
    
    # 可以在这里设置登录凭据
    # 请替换为您的实际邮箱和密码
    email = "huangyuhang2003@gmail.com"  # 在这里填入您的邮箱
    password = "HYH20030210kobe"  # 在这里填入您的密码
    
    # 创建爬虫实例
    crawler = SimpleTemuCrawler(
        keyword="手机配件", 
        max_pages=2,
        email=email,
        password=password
    )
    
    # 开始爬取
    products = crawler.crawl_products()
    
    if products:
        print(f"\n✅ 爬取成功！获取 {len(products)} 个商品")
        crawler.save_results(products)
    else:
        print("\n❌ 爬取失败，未获取到商品数据")
        print("💡 建议:")
        print("  1. 检查网络连接")
        print("  2. 尝试更换关键词")
        print("  3. 减少爬取页数")
        print("  4. 检查登录凭据是否正确")

if __name__ == '__main__':
    main()
