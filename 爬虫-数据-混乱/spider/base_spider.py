"""
基础爬虫类
提供通用的爬虫功能和接口
"""
import time
import random
import logging
import os
import json
import webbrowser
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.safari.webdriver import WebDriver as SafariDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from core.models import SearchConfig, CrawlResult, TemuProduct
from core.utils import get_random_user_agent, random_delay, ensure_directory


class BaseSpider(ABC):
    """基础爬虫抽象类"""
    
    def __init__(self, config: SearchConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver: Optional[webdriver.Chrome] = None
        self.debug_dir = ensure_directory('temu_debug')
        self.cookies_file = os.path.join(self.debug_dir, 'temu_cookies.json')
        
    def __enter__(self):
        """上下文管理器入口"""
        self.setup_driver()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.cleanup()
    
    def setup_driver(self) -> None:
        """设置WebDriver"""
        try:
            # 不使用Safari，使用主机自带的默认浏览器打开
            if getattr(self.config, 'browser', None) == 'system-default':
                start_url = getattr(self.config, 'start_url', 'https://www.example.com')
                webbrowser.open(start_url)
                self.logger.info(f"已在系统默认浏览器打开: {start_url}")
                self.driver = None  # 无法通过Selenium控制，需要手动操作
                return
            else:
                opts = Options()
                if self.config.headless:
                    opts.add_argument("--headless=new")
                
                # 基础配置
                opts.add_argument("--disable-gpu")
                opts.add_argument("--window-size=1920,1080")
                opts.add_argument("--no-sandbox")
                opts.add_argument("--disable-dev-shm-usage")
                opts.add_argument("--disable-blink-features=AutomationControlled")
                opts.add_argument("--disable-infobars")
                opts.add_argument("--start-maximized")
                opts.add_argument("--disable-notifications")
                
                # 设置User-Agent
                user_agent = get_random_user_agent()
                opts.add_argument(f"--user-agent={user_agent}")
                self.logger.info(f"使用User-Agent: {user_agent}")
                
                # 反检测配置（Chrome）
                opts.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
                opts.add_experimental_option("useAutomationExtension", False)
                
                # 初始化Chrome WebDriver
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=opts)
            
            # 增强反检测
            self._enhance_anti_detection()
            
            self.logger.info("WebDriver初始化成功")
            
        except Exception as e:
            self.logger.error(f"WebDriver初始化失败: {e}")
            raise
    
    def _enhance_anti_detection(self) -> None:
        """增强反检测措施"""
        if not self.driver:
            return
        
        try:
            # 隐藏webdriver特征
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'platform', {get: () => ['Win32', 'MacIntel', 'Linux x86_64'][Math.floor(Math.random() * 3)]});
                Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en-US', 'en']});
                Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => [4, 8, 12][Math.floor(Math.random() * 3)]});
                window.navigator.chrome = {runtime: {}, ...window.navigator.chrome};
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3].map(() => ({}))});
                """
            })
            
            # 设置网络请求头
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
                "headers": {
                    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                    "accept-encoding": "gzip, deflate, br",
                    "dnt": "1",
                    "upgrade-insecure-requests": "1"
                }
            })
            
            self.logger.info("反检测措施已应用")
            
        except Exception as e:
            self.logger.warning(f"应用反检测措施失败: {e}")
    
    def simulate_human_behavior(self) -> None:
        """模拟人类行为"""
        if not self.driver:
            return
        
        try:
            # 随机延迟
            random_delay(1, 3)
            
            # 随机滚动
            for _ in range(random.randint(2, 4)):
                scroll_height = random.uniform(0.3, 0.7)
                self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {scroll_height});")
                random_delay(1, 2)
            
            # 随机点击
            try:
                clickable_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a, button, div[role="button"]')
                if clickable_elements:
                    element = random.choice(clickable_elements[:5])  # 只选择前5个
                    ActionChains(self.driver).move_to_element(element).pause(0.5).click().perform()
                    random_delay(1, 2)
            except:
                pass
                
        except Exception as e:
            self.logger.warning(f"模拟人类行为失败: {e}")
    
    def wait_for_page_load(self, timeout: int = 10) -> bool:
        """等待页面加载完成"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except Exception as e:
            self.logger.warning(f"等待页面加载超时: {e}")
            return False
    
    def save_debug_info(self, html: str, page_title: str = "") -> None:
        """保存调试信息"""
        if not self.config.save_debug:
            return
        
        try:
            timestamp = int(time.time())
            
            # 保存HTML
            html_file = f"{self.debug_dir}/temu_page_debug_{timestamp}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(f"<!-- 页面标题: {page_title} -->\n")
                f.write(f"<!-- 页面URL: {self.driver.current_url if self.driver else '未知'} -->\n")
                f.write(html)
            
            self.logger.info(f"调试信息已保存到: {html_file}")
            
        except Exception as e:
            self.logger.error(f"保存调试信息失败: {e}")
    
    def cleanup(self) -> None:
        """清理资源"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver已关闭")
            except Exception as e:
                self.logger.error(f"关闭WebDriver失败: {e}")

    # ===== Cookie 持久化 =====
    def save_cookies(self) -> None:
        """保存当前会话cookies到调试目录。"""
        if not self.driver:
            return
        try:
            cookies = self.driver.get_cookies()
            ensure_directory(self.debug_dir)
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Cookies已保存到: {self.cookies_file}")
        except Exception as e:
            self.logger.warning(f"保存cookies失败: {e}")

    def load_cookies(self) -> bool:
        """从调试目录加载cookies并注入浏览器。调用前需先打开temu域名。"""
        if not self.driver:
            return False
        try:
            if not os.path.exists(self.cookies_file):
                return False
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            loaded = 0
            for ck in cookies:
                try:
                    # Selenium 需要删除非必须字段
                    ck_dict = {k: ck[k] for k in ['name', 'value', 'domain', 'path', 'expiry', 'httpOnly', 'secure'] if k in ck}
                    # domain必须匹配当前站点，若为空让浏览器处理
                    self.driver.add_cookie(ck_dict)
                    loaded += 1
                except Exception:
                    continue
            if loaded:
                self.logger.info(f"已注入 {loaded} 个cookies")
                return True
            return False
        except Exception as e:
            self.logger.warning(f"加载cookies失败: {e}")
            return False
    
    @abstractmethod
    def search(self, keyword: str, page: int = 1) -> Optional[str]:
        """搜索方法，子类必须实现"""
        pass
    
    @abstractmethod
    def parse_products(self, html: str) -> List[TemuProduct]:
        """解析产品方法，子类必须实现"""
        pass
    
    def crawl(self) -> CrawlResult:
        """执行爬取任务"""
        all_products = []
        success_pages = 0
        failed_pages = 0
        error_messages = []
        
        try:
            for page in range(1, self.config.max_pages + 1):
                self.logger.info(f"正在爬取第 {page} 页...")
                
                try:
                    # 搜索页面
                    html = self.search(self.config.keyword, page)
                    if not html:
                        self.logger.warning(f"第 {page} 页获取失败")
                        failed_pages += 1
                        continue
                    
                    # 解析产品
                    products = self.parse_products(html)
                    if products:
                        all_products.extend(products)
                        success_pages += 1
                        self.logger.info(f"第 {page} 页解析到 {len(products)} 个产品")
                    else:
                        self.logger.warning(f"第 {page} 页未解析到产品")
                        failed_pages += 1
                    
                    # 页面间延迟
                    if page < self.config.max_pages:
                        delay = random.uniform(self.config.delay_min, self.config.delay_max)
                        self.logger.info(f"等待 {delay:.2f} 秒后爬取下一页...")
                        time.sleep(delay)
                        
                except Exception as e:
                    error_msg = f"第 {page} 页爬取失败: {str(e)}"
                    self.logger.error(error_msg)
                    error_messages.append(error_msg)
                    failed_pages += 1
                    continue
            
            self.logger.info(f"爬取完成，共获取 {len(all_products)} 个产品")
            
        except Exception as e:
            error_msg = f"爬取过程发生错误: {str(e)}"
            self.logger.error(error_msg)
            error_messages.append(error_msg)
        
        return CrawlResult(
            products=all_products,
            total_count=len(all_products),
            success_pages=success_pages,
            failed_pages=failed_pages,
            error_messages=error_messages
        )
