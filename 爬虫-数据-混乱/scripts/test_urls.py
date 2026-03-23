"""
测试URL生成器
验证生成的URL是否正确
"""
from core.url_generator import TemuURLGenerator
import urllib.parse


def test_url_generation():
    """测试URL生成"""
    generator = TemuURLGenerator()
    
    # 测试手机配件关键词
    keyword = "手机配件"
    urls = generator.generate_search_urls(keyword, 1)
    
    print("=== Temu URL生成测试 ===")
    print(f"关键词: {keyword}")
    print(f"生成的URL数量: {len(urls)}")
    print()
    
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")
        
        # 解析URL参数
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        
        print(f"   路径: {parsed.path}")
        print(f"   参数: {list(params.keys())}")
        if 'search_key' in params:
            decoded_keyword = urllib.parse.unquote(params['search_key'][0])
            print(f"   解码关键词: {decoded_keyword}")
        print()
    
    # 测试URL编码
    print("=== URL编码测试 ===")
    test_keywords = ["手机配件", "蓝牙耳机", "充电器", "手机壳"]
    for kw in test_keywords:
        encoded = urllib.parse.quote(kw)
        decoded = urllib.parse.unquote(encoded)
        print(f"原文: {kw}")
        print(f"编码: {encoded}")
        print(f"解码: {decoded}")
        print(f"正确: {kw == decoded}")
        print()


if __name__ == "__main__":
    test_url_generation()
