"""
Temu爬虫使用示例
展示如何使用重构后的爬虫系统
"""
import logging
from core.models import SearchConfig
from spider.temu_spider import TemuSpider
from core.utils import setup_logging


def example_basic_usage():
    """基础使用示例"""
    print("=== Temu爬虫基础使用示例 ===")
    
    # 设置日志
    logger = setup_logging("INFO")
    
    # 创建搜索配置
    config = SearchConfig(
        keyword="手机配件",
        max_pages=1,
        delay_min=2.0,
        delay_max=4.0,
        headless=True,
        save_debug=True
    )
    
    # 使用上下文管理器运行爬虫
    with TemuSpider(config) as spider:
        result = spider.crawl()
        
        # 显示结果
        print(f"爬取完成！")
        print(f"总产品数: {result.total_count}")
        print(f"成功页数: {result.success_pages}")
        print(f"失败页数: {result.failed_pages}")
        
        # 显示前3个产品
        if result.products:
            print("\n前3个产品:")
            for i, product in enumerate(result.products[:3], 1):
                print(f"{i}. {product.title}")
                print(f"   价格: {product.price}")
                print(f"   链接: {product.product_url}")
                print()
        
        # 保存结果
        spider.save_results(result, config.keyword)


def example_advanced_usage():
    """高级使用示例"""
    print("=== Temu爬虫高级使用示例 ===")
    
    # 设置日志
    logger = setup_logging("DEBUG")
    
    # 创建多个搜索任务
    keywords = ["手机壳", "充电器", "耳机"]
    
    for keyword in keywords:
        print(f"\n正在爬取: {keyword}")
        
        config = SearchConfig(
            keyword=keyword,
            max_pages=1,
            delay_min=3.0,
            delay_max=6.0,
            headless=True,
            save_debug=True
        )
        
        with TemuSpider(config) as spider:
            result = spider.crawl()
            
            if result.products:
                print(f"  - 获取到 {len(result.products)} 个产品")
                # 显示第一个产品
                first_product = result.products[0]
                print(f"  - 示例: {first_product.title} - {first_product.price}")
            else:
                print(f"  - 未获取到产品")
            
            # 保存结果
            spider.save_results(result, keyword)


def example_custom_config():
    """自定义配置示例"""
    print("=== 自定义配置示例 ===")
    
    # 创建自定义配置
    config = SearchConfig(
        keyword="蓝牙耳机",
        max_pages=2,  # 爬取2页
        delay_min=1.0,  # 最小延迟1秒
        delay_max=3.0,  # 最大延迟3秒
        headless=False,  # 显示浏览器窗口
        save_debug=True
    )
    
    print(f"配置信息:")
    print(f"  关键词: {config.keyword}")
    print(f"  页数: {config.max_pages}")
    print(f"  延迟: {config.delay_min}-{config.delay_max}秒")
    print(f"  无头模式: {config.headless}")
    
    with TemuSpider(config) as spider:
        result = spider.crawl()
        
        print(f"\n爬取结果:")
        print(f"  总产品数: {result.total_count}")
        
        if result.error_messages:
            print(f"  错误信息: {len(result.error_messages)} 个")
            for error in result.error_messages:
                print(f"    - {error}")


if __name__ == "__main__":
    # 运行示例
    try:
        example_basic_usage()
        print("\n" + "="*50)
        example_advanced_usage()
        print("\n" + "="*50)
        example_custom_config()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        logging.error(f"示例运行失败: {e}")
