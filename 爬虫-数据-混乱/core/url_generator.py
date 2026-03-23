"""
Temu URL生成器
根据Temu的实际URL格式生成正确的搜索链接
"""
import urllib.parse
import time
import random
from typing import List


class TemuURLGenerator:
    """Temu URL生成器"""
    
    def __init__(self):
        self.base_domain = "https://www.temu.com"
    
    def generate_search_urls(self, keyword: str, page: int = 1) -> List[str]:
        """生成Temu搜索URL列表"""
        # URL编码关键词
        encoded_keyword = urllib.parse.quote(keyword)
        
        # 生成时间戳和会话ID
        timestamp = int(time.time() * 1000)
        session_id = self._generate_session_id()
        
        urls = [
            # 主要搜索URL格式（基于您提供的实际URL）
            f"{self.base_domain}/search_result.html?search_key={encoded_keyword}&search_method=user&refer_page_el_sn=200010&srch_enter_source=top_search_entrance_10005&refer_page_name=home&refer_page_id=10005_{timestamp}_{session_id}&refer_page_sn=10005&_x_sessn_id={session_id}",
            
            # 简化版本（最可能成功的格式）
            f"{self.base_domain}/search_result.html?search_key={encoded_keyword}&search_method=user",
            
            # 带分页的版本
            f"{self.base_domain}/search_result.html?search_key={encoded_keyword}&search_method=user&page={page}",
            
            # 备用URL格式
            f"{self.base_domain}/search?q={encoded_keyword}&page={page}",
            f"{self.base_domain}/hw/search.html?q={encoded_keyword}&page={page}",
        ]
        
        return urls
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        import string
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(10))
    
    def generate_category_urls(self, category: str) -> List[str]:
        """生成分类页面URL"""
        encoded_category = urllib.parse.quote(category)
        
        urls = [
            f"{self.base_domain}/category/{encoded_category}.html",
            f"{self.base_domain}/category/{encoded_category}",
            f"{self.base_domain}/search_result.html?search_key={encoded_category}&search_method=category"
        ]
        
        return urls
    
    def generate_product_url(self, product_id: str) -> str:
        """生成产品详情页URL"""
        return f"{self.base_domain}/p-{product_id}.html"
    
    def add_common_params(self, base_url: str) -> str:
        """为URL添加常用参数"""
        params = {
            'refer_page_name': 'home',
            'refer_page_sn': '10005',
            'srch_enter_source': 'top_search_entrance_10005'
        }
        
        # 解析现有参数
        parsed = urllib.parse.urlparse(base_url)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        # 添加新参数
        for key, value in params.items():
            query_params[key] = [value]
        
        # 重新构建URL
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        new_url = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, new_query, parsed.fragment
        ))
        
        return new_url
