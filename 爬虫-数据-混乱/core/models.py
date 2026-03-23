"""
Temu爬虫数据模型
定义产品信息的数据结构
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class TemuProduct:
    """Temu产品信息数据模型"""
    title: str                    # 产品标题
    price: str                    # 价格
    discount: str                # 折扣信息
    listing_date: str            # 上架日期
    product_url: str             # 产品链接
    original_price: Optional[str] = None  # 原价
    rating: Optional[str] = None          # 评分
    sales_count: Optional[str] = None     # 销量
    image_url: Optional[str] = None        # 图片链接
    category: Optional[str] = None         # 分类
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'title': self.title,
            'price': self.price,
            'discount': self.discount,
            'listing_date': self.listing_date,
            'product_url': self.product_url,
            'original_price': self.original_price,
            'rating': self.rating,
            'sales_count': self.sales_count,
            'image_url': self.image_url,
            'category': self.category
        }
    
    def to_csv_row(self) -> str:
        """转换为CSV行格式"""
        return f'"{self.title}","{self.price}","{self.discount}","{self.listing_date}","{self.product_url}","{self.original_price}","{self.rating}","{self.sales_count}","{self.image_url}","{self.category}"'
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TemuProduct':
        """从字典创建产品对象"""
        return cls(
            title=data.get('title', ''),
            price=data.get('price', ''),
            discount=data.get('discount', ''),
            listing_date=data.get('listing_date', ''),
            product_url=data.get('product_url', ''),
            original_price=data.get('original_price'),
            rating=data.get('rating'),
            sales_count=data.get('sales_count'),
            image_url=data.get('image_url'),
            category=data.get('category')
        )


@dataclass
class SearchConfig:
    """搜索配置"""
    keyword: str                  # 搜索关键词
    max_pages: int = 1           # 最大页数
    delay_min: float = 2.0       # 最小延迟时间（秒）
    delay_max: float = 5.0       # 最大延迟时间（秒）
    use_proxy: bool = False       # 是否使用代理
    headless: bool = True         # 是否无头模式
    save_debug: bool = True       # 是否保存调试信息
    manual_unlock: bool = False   # 检测到登录/验证码时允许手动解锁
    browser: str = 'chrome'       # 浏览器类型（当前仅使用chrome驱动）
    open_in_default: bool = False # 爬取时同时在系统默认浏览器中打开页面（仅展示）


@dataclass
class CrawlResult:
    """爬取结果"""
    products: list[TemuProduct]   # 产品列表
    total_count: int             # 总数量
    success_pages: int           # 成功页数
    failed_pages: int            # 失败页数
    error_messages: list[str]    # 错误信息
    
    def __post_init__(self):
        self.total_count = len(self.products)
