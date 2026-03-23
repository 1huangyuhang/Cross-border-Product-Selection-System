"""
Temu爬虫实现
专门用于爬取Temu网站的产品信息
"""
import time
import random
import logging
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from .base_spider import BaseSpider
from core.models import SearchConfig, TemuProduct
from .temu_parser import TemuParser
from core.url_generator import TemuURLGenerator
from core.utils import random_delay, save_json, save_csv, format_timestamp


class TemuSpider(BaseSpider):
    """Temu爬虫实现类"""
    
    def __init__(self, config: SearchConfig):
        super().__init__(config)
        self.parser = TemuParser()
        self.url_generator = TemuURLGenerator()
    
    def search(self, keyword: str, page: int = 1) -> Optional[str]:
        """搜索Temu商品"""
        if not self.driver:
            self.logger.error("WebDriver未初始化")
            return None
        
        try:
            # 使用URL生成器生成正确的Temu搜索URL
            urls = self.url_generator.generate_search_urls(keyword, page)
            url = random.choice(urls)
            
            self.logger.info(f"访问URL: {url}")
            
            # 随机选择访问策略
            if random.random() > 0.3:
                # 策略1: 先访问主页再搜索
                self._visit_homepage_first()
                self._perform_search(keyword)
            else:
                # 策略2: 直接访问搜索URL
                self.driver.get(url)
            
            # 可选：同步在系统默认浏览器中打开当前URL，便于肉眼观察
            try:
                if getattr(self.config, 'open_in_default', False):
                    import webbrowser
                    webbrowser.open_new_tab(self.driver.current_url)
            except Exception:
                pass
            
            # 等待页面加载
            self.wait_for_page_load()
            
            # 模拟人类行为
            self.simulate_human_behavior()
            
            # 检查是否被重定向到登录/验证码页面
            if self._is_redirected_to_login():
                self.logger.warning("被重定向到登录/验证页面")
                # 若允许手动解锁，先等待用户完成
                if self._wait_manual_unlock_if_needed():
                    pass
                else:
                    self.logger.info("尝试自动绕过...")
                    if not self._bypass_login_redirect(keyword, page):
                        return None
            
            # 等待商品列表加载：分段滚动促发懒加载
            try:
                total = 8
                for i in range(total):
                    self.driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight * arguments[0] / arguments[1]);",
                        i + 1, total
                    )
                    time.sleep(random.uniform(0.8, 1.6))
            except Exception:
                pass
            self._wait_for_product_list()
            
            # 获取页面源码
            html = self.driver.page_source
            self.logger.info(f"成功获取第{page}页数据")
            # 成功后保存cookies以便下次复用
            try:
                self.save_cookies()
            except Exception:
                pass
            
            return html
            
        except Exception as e:
            self.logger.error(f"搜索失败: {e}")
            return None
    
    def _visit_homepage_first(self) -> None:
        """先访问主页"""
        try:
            self.driver.get("https://www.temu.com/")
            # 先尝试加载历史cookies再刷新
            try:
                if self.load_cookies():
                    self.driver.refresh()
            except Exception:
                pass
            random_delay(2, 4)
            self.simulate_human_behavior()
        except Exception as e:
            self.logger.warning(f"访问主页失败: {e}")
    
    def _perform_search(self, keyword: str) -> None:
        """执行搜索"""
        try:
            # 尝试多种搜索框选择器，增加更多可能的定位方式
            search_selectors = [
                '#searchInput',               # 你提供的真实id
                'input[role="searchbox"]',   # 语义role
                'input[type="search"]',
                '[name="q"]',
                '#search-input',
                '[placeholder*="搜索"]',
                '[placeholder*="search"]',
                'input[autocomplete="off"]',  # 常见的搜索框属性
                'input[class*="search"]',     # 包含search的class
                'input[id*="search"]',        # 包含search的id
                'input[aria-label*="搜索"]',  # aria-label包含搜索
                'input[aria-label*="search"]', # aria-label包含search
                'input[class*="input"]',      # 包含input的class
                'input[placeholder*="输入"]', # 包含"输入"的placeholder
                'input[placeholder*="Enter"]', # 包含"Enter"的placeholder
                'input[class*="text"]',       # 包含text的class
                'input[type="text"]',         # 普通文本输入框
                'input[class*="form"]',       # 包含form的class
                'input[class*="field"]'      # 包含field的class
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if search_box.is_displayed() and search_box.is_enabled():
                        self.logger.info(f"找到搜索框: {selector}")
                        break
                except:
                    continue
            
            if search_box:
                # 点击搜索框
                ActionChains(self.driver).move_to_element(search_box).pause(0.5).click().perform()
                random_delay(0.5, 1)
                
                # searchInput 可能带 disabled，需要去掉disabled后输入
                try:
                    self.driver.execute_script("arguments[0].removeAttribute('disabled');", search_box)
                except Exception:
                    pass
                # 清空并输入关键词
                try:
                    search_box.clear()
                except Exception:
                    pass
                self._type_like_human(search_box, keyword)
                
                # 提交搜索
                if random.random() > 0.5:
                    search_box.send_keys("\n")
                else:
                    self._click_search_button()
            else:
                self.logger.warning("未找到搜索框，使用直接URL访问")
                
        except Exception as e:
            self.logger.warning(f"执行搜索失败: {e}")
    
    def _type_like_human(self, element, text: str) -> None:
        """模拟人类打字"""
        for i, char in enumerate(text):
            element.send_keys(char)
            delay = random.uniform(0.05, 0.2)
            # 每打几个字符可能会停顿
            if i > 0 and i % random.randint(3, 5) == 0:
                delay += random.uniform(0.5, 1.5)
            time.sleep(delay)
    
    def _click_search_button(self) -> None:
        """点击搜索按钮"""
        try:
            search_button_selectors = [
                'button[type="submit"]',
                '[class*="search-btn"]',
                '[class*="search-button"]',
                'button:contains("搜索")',
                'button:contains("search")'
            ]
            
            for selector in search_button_selectors:
                try:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if button.is_displayed():
                        ActionChains(self.driver).move_to_element(button).pause(0.5).click().perform()
                        self.logger.info("已点击搜索按钮")
                        return
                except:
                    continue
        except Exception as e:
            self.logger.warning(f"点击搜索按钮失败: {e}")
    
    def _is_redirected_to_login(self) -> bool:
        """检查是否被重定向到登录页面"""
        try:
            current_url = self.driver.current_url.lower()
            page_title = self.driver.title.lower()
            page_source = self.driver.page_source.lower()
            
            login_indicators = ['login', '登录', 'signin', 'sign-in', 'captcha', '验证码']
            
            return any(indicator in current_url or indicator in page_title or indicator in page_source 
                      for indicator in login_indicators)
        except:
            return False
    
    def _bypass_login_redirect(self, keyword: str, page: int) -> bool:
        """尝试绕过登录重定向"""
        try:
            # 使用URL生成器生成绕过URL
            bypass_urls = self.url_generator.generate_search_urls(keyword, page)
            
            for url in bypass_urls:
                self.logger.info(f"尝试绕过URL: {url}")
                self.driver.get(url)
                random_delay(3, 6)
                
                if not self._is_redirected_to_login():
                    self.logger.info("成功绕过登录重定向")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"绕过登录重定向失败: {e}")
            return False

    def _wait_manual_unlock_if_needed(self) -> bool:
        """如果配置了manual_unlock，在检测到登录/验证码时，提示用户手动完成后继续。"""
        if not getattr(self.config, 'manual_unlock', False):
            return False
        try:
            self.logger.info("检测到需要手动解锁，请在浏览器中完成登录/验证码，然后返回继续...")
            # 给用户最多300秒完成（根据网络/设备情况放宽）
            import time
            deadline = time.time() + 300
            while time.time() < deadline:
                if not self._is_redirected_to_login():
                    self.logger.info("已检测到页面可访问，继续爬取")
                    return True
                time.sleep(3)
            self.logger.warning("等待手动解锁超时")
            return False
        except Exception as e:
            self.logger.warning(f"手动解锁等待失败: {e}")
            return False
    
    def _wait_for_product_list(self) -> None:
        """等待商品列表加载"""
        try:
            # 尝试多种商品选择器
            product_selectors = [
                '[data-sqe="product-item"]',
                'div[data-sqe="product-item"]',
                'div[class*="product-item"]',
                'div[class*="product"]',
                'a[href*="/p-"]',
                'a[href*="/goods.html?"]',
                'a[href*="/p-" i]'
            ]
            
            for selector in product_selectors:
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    self.logger.info(f"商品列表加载完成，使用选择器: {selector}")
                    return
                except:
                    continue
            
            self.logger.warning("未检测到商品列表元素")
            
        except Exception as e:
            self.logger.warning(f"等待商品列表加载失败: {e}")
    
    def parse_products(self, html: str) -> List[TemuProduct]:
        """解析产品信息"""
        return self.parser.parse_search_page(html)
    
    def save_results(self, result: 'CrawlResult', keyword: str) -> None:
        """保存爬取结果"""
        if not result.products:
            self.logger.warning("没有产品数据可保存")
            return
        
        timestamp = format_timestamp()
        
        # 保存为JSON格式
        json_file = f"{self.debug_dir}/temu_{keyword}_products_{timestamp}.json"
        products_data = [product.to_dict() for product in result.products]
        if save_json(products_data, json_file):
            self.logger.info(f"JSON数据已保存到: {json_file}")
        
        # 保存为CSV格式
        csv_file = f"{self.debug_dir}/temu_{keyword}_products_{timestamp}.csv"
        headers = ['title', 'price', 'discount', 'listing_date', 'product_url', 
                  'original_price', 'rating', 'sales_count', 'image_url', 'category']
        if save_csv(products_data, csv_file, headers):
            self.logger.info(f"CSV数据已保存到: {csv_file}")
        
        # 保存汇总信息
        summary = {
            'keyword': keyword,
            'total_products': result.total_count,
            'success_pages': result.success_pages,
            'failed_pages': result.failed_pages,
            'error_messages': result.error_messages,
            'timestamp': timestamp
        }
        
        summary_file = f"{self.debug_dir}/temu_{keyword}_summary_{timestamp}.json"
        if save_json(summary, summary_file):
            self.logger.info(f"汇总信息已保存到: {summary_file}")


def create_spider(keyword: str, max_pages: int = 1, **kwargs) -> TemuSpider:
    """创建Temu爬虫实例的工厂函数"""
    config = SearchConfig(
        keyword=keyword,
        max_pages=max_pages,
        delay_min=kwargs.get('delay_min', 2.0),
        delay_max=kwargs.get('delay_max', 5.0),
        use_proxy=kwargs.get('use_proxy', False),
        headless=kwargs.get('headless', True),
        save_debug=kwargs.get('save_debug', True)
    )
    return TemuSpider(config)
