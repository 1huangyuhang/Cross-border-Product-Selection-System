"""
Temu页面解析器
专门用于解析Temu网站的产品信息
"""
import re
import json
import logging
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
from core.models import TemuProduct
from core.utils import clean_text, extract_price_number, validate_url, extract_json_from_html


class TemuParser:
    """Temu页面解析器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def parse_search_page(self, html: str) -> List[TemuProduct]:
        """解析搜索页面，提取产品信息"""
        products = []
        
        if not html:
            self.logger.warning("HTML内容为空")
            return products
        
        # 检查是否是登录页面
        if self._is_login_page(html):
            self.logger.warning("检测到登录页面，无法解析产品信息")
            return products
        
        # 尝试多种解析方法
        products = self._parse_from_json(html)
        if products:
            self.logger.info(f"从JSON数据解析到 {len(products)} 个产品")
            return products
        
        products = self._parse_from_html(html)
        if products:
            self.logger.info(f"从HTML解析到 {len(products)} 个产品")
            return products
        
        self.logger.warning("未能解析到任何产品信息")
        return products
    
    def _is_login_page(self, html: str) -> bool:
        """检查是否是登录页面"""
        login_indicators = [
            '登录', 'login', 'signin', 'sign-in', 
            'captcha', '验证码', 'verification'
        ]
        html_lower = html.lower()
        return any(indicator in html_lower for indicator in login_indicators)
    
    def _parse_from_json(self, html: str) -> List[TemuProduct]:
        """从JSON数据中解析产品信息"""
        json_markers = [
            ('window.__INITIAL_STATE__ = ', ';</script>'),
            ('window.__DATA__ = ', ';</script>'),
            ('window.__PRODUCTS__ = ', ';</script>'),
            ('<script id="__NEXT_DATA__" type="application/json">', '</script>'),
            ('window.__REDUX_STATE__ = ', ';</script>'),
            ('window.__APP_STATE__ = ', ';</script>'),
            ('window.__SEARCH_RESULT__ = ', ';</script>'),
            ('<script id="__SEARCH_DATA__" type="application/json">', '</script>'),
            ('window.initialData = ', ';</script>'),
            ('window.storeData = ', ';</script>'),
            ('window.globalData = ', ';</script>'),
            ('<script id="search-data" type="application/json">', '</script>'),
            ('window.data = ', ';</script>'),
            ('window._initialState = ', ';</script>'),
            ('<script id="__APOLLO_STATE__" type="application/json">', '</script>')
        ]
        
        for start_marker, end_marker in json_markers:
            json_data = extract_json_from_html(html, start_marker, end_marker)
            if json_data:
                products = self._extract_products_from_json(json_data)
                if products:
                    return products
        
        return []
    
    
    def _extract_products_from_json(self, json_data: Dict) -> List[TemuProduct]:
        """从JSON数据中提取产品信息"""
        products = []
        
        # 尝试在JSON数据的不同位置寻找商品列表
        search_paths = [
            ['products'],
            ['data', 'products'],
            ['result', 'products'],
            ['searchResult', 'items'],
            ['pageData', 'products'],
            ['pageProps', 'products'],
            ['props', 'pageProps', 'products'],
            ['items'],
            ['listItems'],
            ['data', 'items'],
            ['result', 'items'],
            ['payload', 'items'],
            ['data', 'searchResult', 'items'],
            ['data', 'productsList', 'items'],
            ['goodsList', 'items'],
            ['search_list', 'items'],
            ['search_result', 'items'],
            ['content', 'items'],
            ['searchData', 'items'],
            ['data', 'itemList', 'items'],
            ['itemList', 'items'],
            ['resultList', 'items'],
            ['products', 'items'],
            ['productList', 'items'],
            ['search', 'results', 'items'],
            ['searchResults', 'hits'],
            ['hits'],
            ['data', 'hits'],
            ['items', 'list'],
            ['data', 'list'],
            ['pageData', 'list'],
            ['result', 'list'],
            ['content', 'list']
        ]
        
        for path in search_paths:
            try:
                data = json_data
                for key in path:
                    data = data[key]
                
                if isinstance(data, list):
                    self.logger.info(f"在路径 {path} 找到商品列表，共 {len(data)} 个商品")
                    
                    for item in data:
                        product = self._parse_product_from_json_item(item)
                        if product:
                            products.append(product)
                    
                    if products:
                        return products
            except (KeyError, TypeError):
                continue
        
        return products
    
    def _parse_product_from_json_item(self, item: Dict) -> Optional[TemuProduct]:
        """从JSON商品项中解析产品信息"""
        try:
            # 提取基本信息
            title = self._extract_field(item, [
                'name', 'title', 'goodsName', 'productName', 
                'displayName', 'name_en', 'name_cn', 'itemName'
            ])
            
            price = self._extract_field(item, [
                'price', 'currentPrice', 'discountPrice', 
                'finalPrice', 'salePrice', 'value', 'amount'
            ])
            
            original_price = self._extract_field(item, [
                'originalPrice', 'listPrice', 'marketPrice', 'oldPrice'
            ])
            
            discount = self._extract_field(item, [
                'discount', 'discountRate', 'discountPercent', 'sale'
            ])
            
            product_url = self._extract_field(item, [
                'url', 'link', 'href', 'productUrl', 'detailUrl'
            ])
            
            rating = self._extract_field(item, [
                'rating', 'score', 'stars', 'reviewScore'
            ])
            
            sales_count = self._extract_field(item, [
                'sales', 'soldCount', 'orderCount', 'salesVolume', 
                'volume', 'count', 'quantity'
            ])
            
            image_url = self._extract_field(item, [
                'image', 'imageUrl', 'img', 'picture', 'photo'
            ])
            
            listing_date = self._extract_field(item, [
                'listingDate', 'createDate', 'publishDate', 'date'
            ])
            
            category = self._extract_field(item, [
                'category', 'categoryName', 'type', 'class'
            ])
            
            # 验证必要字段
            if not title or not product_url:
                return None
            
            # 确保URL格式正确
            if not validate_url(product_url):
                if not product_url.startswith('http'):
                    product_url = f"https://www.temu.com{product_url}"
            
            return TemuProduct(
                title=clean_text(title),
                price=clean_text(price) if price else "",
                discount=clean_text(discount) if discount else "",
                listing_date=clean_text(listing_date) if listing_date else "",
                product_url=product_url,
                original_price=clean_text(original_price) if original_price else None,
                rating=clean_text(rating) if rating else None,
                sales_count=clean_text(sales_count) if sales_count else None,
                image_url=clean_text(image_url) if image_url else None,
                category=clean_text(category) if category else None
            )
            
        except Exception as e:
            self.logger.error(f"解析JSON商品项失败: {e}")
            return None
    
    def _extract_field(self, item: Dict, field_names: List[str]) -> Optional[str]:
        """从字典中提取字段值"""
        for field_name in field_names:
            if field_name in item and item[field_name]:
                return str(item[field_name])
        return None
    
    def _parse_from_html(self, html: str) -> List[TemuProduct]:
        """从HTML中解析产品信息"""
        products = []
        
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # 尝试多种可能的产品选择器
            product_selectors = [
                '[data-sqe="product-item"]',
                'div[data-sqe="product-item"]',
                'div.sx5l94g',  # 常见的Temu商品容器类名
                'div[class*="product-item"]',
                'div[class*="product"]',
                'div[data-category="product"]',
                'div.product-card',
                'a[href*="product"]',
                'div[class^="styles_product-item_"]',
                'div[class*="search-item"]',
                'li[class*="product"]',
                'div[itemtype="http://schema.org/Product"]',
                'div[class*="goods-item"]',
                'div[class*="item-container"]',
                'a[href*="/p-"]'  # Temu产品链接格式
            ]
            
            product_items = []
            for selector in product_selectors:
                items = soup.select(selector)
                if items:
                    product_items = items
                    self.logger.info(f"使用选择器 '{selector}' 找到 {len(product_items)} 个商品项")
                    break
            
            if not product_items:
                self.logger.warning("未找到商品项")
                return products
            
            # 解析每个商品项
            for item in product_items:
                product = self._parse_product_from_html_item(item)
                if product:
                    products.append(product)
            
        except Exception as e:
            self.logger.error(f"解析HTML失败: {e}")
        
        return products
    
    def _parse_product_from_html_item(self, item) -> Optional[TemuProduct]:
        """从HTML商品项中解析产品信息"""
        try:
            # 提取标题
            title = self._extract_text_from_element(item, [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                '[class*="title"]', '[class*="name"]',
                '[class*="product-name"]', '[class*="goods-name"]'
            ])
            
            # 提取价格
            price = self._extract_price_from_element(item)
            
            # 提取原价
            original_price = self._extract_original_price_from_element(item)
            
            # 提取折扣
            discount = self._extract_discount_from_element(item)
            
            # 提取链接
            product_url = self._extract_url_from_element(item)
            
            # 提取评分
            rating = self._extract_rating_from_element(item)
            
            # 提取销量
            sales_count = self._extract_sales_from_element(item)
            
            # 提取图片
            image_url = self._extract_image_from_element(item)
            
            # 提取上架日期
            listing_date = self._extract_date_from_element(item)
            
            # 提取分类
            category = self._extract_category_from_element(item)
            
            # 验证必要字段
            if not title or not product_url:
                return None
            
            # 确保URL格式正确
            if not validate_url(product_url):
                if not product_url.startswith('http'):
                    product_url = f"https://www.temu.com{product_url}"
            
            return TemuProduct(
                title=clean_text(title),
                price=clean_text(price) if price else "",
                discount=clean_text(discount) if discount else "",
                listing_date=clean_text(listing_date) if listing_date else "",
                product_url=product_url,
                original_price=clean_text(original_price) if original_price else None,
                rating=clean_text(rating) if rating else None,
                sales_count=clean_text(sales_count) if sales_count else None,
                image_url=clean_text(image_url) if image_url else None,
                category=clean_text(category) if category else None
            )
            
        except Exception as e:
            self.logger.error(f"解析HTML商品项失败: {e}")
            return None
    
    def _extract_text_from_element(self, element, selectors: List[str]) -> Optional[str]:
        """从元素中提取文本"""
        for selector in selectors:
            try:
                found = element.select_one(selector)
                if found and found.get_text(strip=True):
                    return found.get_text(strip=True)
            except:
                continue
        return None
    
    def _extract_price_from_element(self, element) -> Optional[str]:
        """从元素中提取价格"""
        # 查找包含货币符号的元素
        currency_symbols = ['$', '¥', '£', '€', '¢', 'USD', 'CNY']
        for symbol in currency_symbols:
            try:
                price_elements = element.find_all(text=re.compile(f'\\{symbol}'))
                for price_text in price_elements:
                    if price_text.strip():
                        return price_text.strip()
            except:
                continue
        
        # 查找包含数字和小数点的元素
        try:
            import re
            all_text = element.get_text()
            price_pattern = r'\d+\.?\d*'
            matches = re.findall(price_pattern, all_text)
            if matches:
                return matches[0]
        except:
            pass
        
        return None
    
    def _extract_original_price_from_element(self, element) -> Optional[str]:
        """从元素中提取原价"""
        original_price_selectors = [
            '[class*="original-price"]',
            '[class*="old-price"]',
            '[class*="list-price"]',
            '[class*="market-price"]'
        ]
        return self._extract_text_from_element(element, original_price_selectors)
    
    def _extract_discount_from_element(self, element) -> Optional[str]:
        """从元素中提取折扣信息"""
        discount_selectors = [
            '[class*="discount"]',
            '[class*="sale"]',
            '[class*="off"]',
            '[class*="save"]'
        ]
        return self._extract_text_from_element(element, discount_selectors)
    
    def _extract_url_from_element(self, element) -> Optional[str]:
        """从元素中提取链接"""
        try:
            # 查找链接元素
            link = element.find('a')
            if link and link.get('href'):
                return link.get('href')
            
            # 如果元素本身就是链接
            if element.name == 'a' and element.get('href'):
                return element.get('href')
        except:
            pass
        return None
    
    def _extract_rating_from_element(self, element) -> Optional[str]:
        """从元素中提取评分"""
        rating_selectors = [
            '[class*="rating"]',
            '[class*="score"]',
            '[class*="stars"]',
            '[class*="review"]'
        ]
        return self._extract_text_from_element(element, rating_selectors)
    
    def _extract_sales_from_element(self, element) -> Optional[str]:
        """从元素中提取销量"""
        sales_keywords = ['sold', '销量', '已售', 'sales', 'orders', '已销售', '已卖出']
        all_text = element.get_text().lower()
        for keyword in sales_keywords:
            if keyword in all_text:
                # 尝试提取数字
                import re
                pattern = rf'{keyword}[:\s]*(\d+)'
                match = re.search(pattern, all_text)
                if match:
                    return match.group(1)
        return None
    
    def _extract_image_from_element(self, element) -> Optional[str]:
        """从元素中提取图片链接"""
        try:
            img = element.find('img')
            if img and img.get('src'):
                return img.get('src')
        except:
            pass
        return None
    
    def _extract_date_from_element(self, element) -> Optional[str]:
        """从元素中提取日期"""
        date_selectors = [
            '[class*="date"]',
            '[class*="time"]',
            '[class*="created"]',
            '[class*="published"]'
        ]
        return self._extract_text_from_element(element, date_selectors)
    
    def _extract_category_from_element(self, element) -> Optional[str]:
        """从元素中提取分类"""
        category_selectors = [
            '[class*="category"]',
            '[class*="type"]',
            '[class*="class"]',
            '[class*="tag"]'
        ]
        return self._extract_text_from_element(element, category_selectors)
