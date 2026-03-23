#!/usr/bin/env python3
"""
跨境电商选品系统 - 商品爬虫
按照software.md文档要求实现爬虫模块
"""

import scrapy
import requests
from bs4 import BeautifulSoup
import re
import json
import logging
import time
import random
from datetime import datetime
from urllib.parse import urljoin, urlparse
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductSpider(scrapy.Spider):
    """商品爬虫 - 按照software.md文档要求实现"""
    
    name = 'product_spider'
    allowed_domains = ['temu.com', 'aliexpress.com', 'amazon.com']
    
    def __init__(self, keyword='手机配件', max_pages=10, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.max_pages = max_pages
        self.start_urls = [
            f'https://www.temu.com/search?q={keyword}',
            f'https://www.aliexpress.com/wholesale?SearchText={keyword}',
            f'https://www.amazon.com/s?k={keyword}'
        ]
        self.db_connection = None
        self._init_database()
    
    def _init_database(self):
        """初始化数据库连接"""
        try:
            # 按照software.md文档要求使用PostgreSQL
            self.db_connection = create_engine(
                'postgresql://postgres:password@localhost:5432/ecommerce_db'
            )
            logger.info("数据库连接初始化成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
    
    def start_requests(self):
        """开始请求 - 按照software.md文档要求实现"""
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'page': 1},
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                dont_filter=True
            )
    
    def parse(self, response):
        """解析商品列表页面 - 按照software.md文档要求实现"""
        page = response.meta.get('page', 1)
        domain = urlparse(response.url).netloc
        
        logger.info(f"解析页面 {page}: {response.url}")
        
        # 根据域名选择不同的解析方法
        if 'temu.com' in domain:
            yield from self.parse_temu(response)
        elif 'aliexpress.com' in domain:
            yield from self.parse_aliexpress(response)
        elif 'amazon.com' in domain:
            yield from self.parse_amazon(response)
        
        # 翻页处理
        if page < self.max_pages:
            next_page_url = self.get_next_page_url(response, page + 1)
            if next_page_url:
                yield scrapy.Request(
                    url=next_page_url,
                    callback=self.parse,
                    meta={'page': page + 1},
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                )
    
    def parse_temu(self, response):
        """解析TEMU商品 - 按照software.md文档要求实现"""
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取商品链接
        product_links = soup.select('a[href*="/product/"]')
        
        for link in product_links[:10]:  # 限制数量避免过多请求
            product_url = urljoin(response.url, link.get('href'))
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta={'platform': 'temu'},
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
    
    def parse_aliexpress(self, response):
        """解析AliExpress商品 - 按照software.md文档要求实现"""
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取商品链接
        product_links = soup.select('a[href*="/item/"]')
        
        for link in product_links[:10]:
            product_url = urljoin(response.url, link.get('href'))
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta={'platform': 'aliexpress'},
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
    
    def parse_amazon(self, response):
        """解析Amazon商品 - 按照software.md文档要求实现"""
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取商品链接
        product_links = soup.select('a[href*="/dp/"]')
        
        for link in product_links[:10]:
            product_url = urljoin(response.url, link.get('href'))
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta={'platform': 'amazon'},
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
    
    def parse_product(self, response):
        """解析商品详情页面 - 按照software.md文档要求实现"""
        platform = response.meta.get('platform', 'unknown')
        
        # 使用BeautifulSoup解析商品信息
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取商品信息
        product_data = {
            'platform': platform,
            'url': response.url,
            'crawl_date': datetime.now().isoformat(),
            'title': self.extract_title(soup),
            'price': self.extract_price(soup),
            'original_price': self.extract_original_price(soup),
            'rating': self.extract_rating(soup),
            'review_count': self.extract_review_count(soup),
            'sales_count': self.extract_sales_count(soup),
            'image_url': self.extract_image_url(soup, response.url),
            'description': self.extract_description(soup),
            'category': self.extract_category(soup),
            'brand': self.extract_brand(soup),
            'keywords': self.extract_keywords(soup),
            'is_available': self.check_availability(soup)
        }
        
        # 数据清洗 - 按照software.md文档要求实现
        product_data = self.clean_data(product_data)
        
        # 存储到数据库 - 按照software.md文档要求实现
        self.save_to_database(product_data)
        
        yield product_data
    
    def extract_title(self, soup):
        """提取商品标题"""
        title_selectors = [
            'h1',
            '.product-title',
            '.title',
            '[data-testid="product-title"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        return ''
    
    def extract_price(self, soup):
        """提取商品价格"""
        price_selectors = [
            '.price',
            '.current-price',
            '[data-testid="price"]',
            '.price-current'
        ]
        
        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text()
                # 使用正则表达式提取数字
                price_match = re.search(r'[\d,]+\.?\d*', price_text)
                if price_match:
                    return float(price_match.group().replace(',', ''))
        return 0.0
    
    def extract_original_price(self, soup):
        """提取原价"""
        original_selectors = [
            '.original-price',
            '.price-original',
            '.was-price'
        ]
        
        for selector in original_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text()
                price_match = re.search(r'[\d,]+\.?\d*', price_text)
                if price_match:
                    return float(price_match.group().replace(',', ''))
        return None
    
    def extract_rating(self, soup):
        """提取评分"""
        rating_selectors = [
            '.rating',
            '.stars',
            '[data-testid="rating"]'
        ]
        
        for selector in rating_selectors:
            element = soup.select_one(selector)
            if element:
                rating_text = element.get_text()
                rating_match = re.search(r'[\d.]+', rating_text)
                if rating_match:
                    return float(rating_match.group())
        return 0.0
    
    def extract_review_count(self, soup):
        """提取评论数量"""
        review_selectors = [
            '.review-count',
            '.reviews',
            '[data-testid="review-count"]'
        ]
        
        for selector in review_selectors:
            element = soup.select_one(selector)
            if element:
                count_text = element.get_text()
                count_match = re.search(r'[\d,]+', count_text)
                if count_match:
                    return int(count_match.group().replace(',', ''))
        return 0
    
    def extract_sales_count(self, soup):
        """提取销量"""
        sales_selectors = [
            '.sales-count',
            '.sold',
            '[data-testid="sales"]'
        ]
        
        for selector in sales_selectors:
            element = soup.select_one(selector)
            if element:
                sales_text = element.get_text()
                sales_match = re.search(r'[\d,]+', sales_text)
                if sales_match:
                    return int(sales_match.group().replace(',', ''))
        return 0
    
    def extract_image_url(self, soup, base_url):
        """提取商品图片URL"""
        image_selectors = [
            '.product-image img',
            '.main-image img',
            '[data-testid="product-image"] img'
        ]
        
        for selector in image_selectors:
            element = soup.select_one(selector)
            if element:
                image_url = element.get('src')
                if image_url:
                    return urljoin(base_url, image_url)
        return ''
    
    def extract_description(self, soup):
        """提取商品描述"""
        desc_selectors = [
            '.product-description',
            '.description',
            '[data-testid="description"]'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        return ''
    
    def extract_category(self, soup):
        """提取商品分类"""
        category_selectors = [
            '.breadcrumb a',
            '.category',
            '[data-testid="category"]'
        ]
        
        for selector in category_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        return ''
    
    def extract_brand(self, soup):
        """提取品牌"""
        brand_selectors = [
            '.brand',
            '.manufacturer',
            '[data-testid="brand"]'
        ]
        
        for selector in brand_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        return ''
    
    def extract_keywords(self, soup):
        """提取关键词"""
        keywords = []
        
        # 从标题提取关键词
        title = self.extract_title(soup)
        if title:
            keywords.extend(title.lower().split())
        
        # 从描述提取关键词
        description = self.extract_description(soup)
        if description:
            keywords.extend(description.lower().split())
        
        # 去重并过滤
        keywords = list(set([kw for kw in keywords if len(kw) > 2]))
        return ','.join(keywords[:10])
    
    def check_availability(self, soup):
        """检查商品是否可用"""
        unavailable_indicators = [
            '.out-of-stock',
            '.unavailable',
            '.sold-out'
        ]
        
        for indicator in unavailable_indicators:
            if soup.select_one(indicator):
                return False
        return True
    
    def clean_data(self, data):
        """数据清洗 - 按照software.md文档要求实现"""
        # 清理标题
        if data.get('title'):
            data['title'] = re.sub(r'\s+', ' ', data['title']).strip()
        
        # 清理描述
        if data.get('description'):
            data['description'] = re.sub(r'\s+', ' ', data['description']).strip()
        
        # 确保价格为正数
        if data.get('price') and data['price'] < 0:
            data['price'] = 0.0
        
        if data.get('original_price') and data['original_price'] < 0:
            data['original_price'] = None
        
        # 确保评分为0-5之间
        if data.get('rating'):
            data['rating'] = max(0.0, min(5.0, data['rating']))
        
        return data
    
    def save_to_database(self, product_data):
        """保存到数据库 - 按照software.md文档要求实现"""
        try:
            if self.db_connection:
                # 使用pandas DataFrame保存数据
                df = pd.DataFrame([product_data])
                
                # 按照software.md文档要求使用INSERT INTO
                df.to_sql('products', self.db_connection, if_exists='append', index=False)
                
                logger.info(f"商品数据已保存到数据库: {product_data.get('title', 'Unknown')}")
            else:
                logger.warning("数据库连接不可用，跳过数据保存")
                
        except Exception as e:
            logger.error(f"保存数据到数据库失败: {e}")
    
    def get_next_page_url(self, response, page):
        """获取下一页URL"""
        domain = urlparse(response.url).netloc
        
        if 'temu.com' in domain:
            return f"{response.url}&page={page}"
        elif 'aliexpress.com' in domain:
            return f"{response.url}&page={page}"
        elif 'amazon.com' in domain:
            return f"{response.url}&page={page}"
        
        return None

def main():
    """主函数 - 按照software.md文档要求实现"""
    logger.info("启动商品爬虫模块")
    
    # 这里可以添加爬虫启动逻辑
    # 实际使用中应该通过scrapy命令行启动
    logger.info("爬虫模块初始化完成")

if __name__ == "__main__":
    main()