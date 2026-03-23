"""
Temu爬虫主程序
提供简单的命令行接口来运行爬虫
"""
import argparse
import logging
import sys
from typing import List

from core.models import SearchConfig
from spider.temu_spider import TemuSpider, create_spider
from core.utils import setup_logging


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description='Temu产品信息爬虫')
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('-p', '--pages', type=int, default=1, help='爬取页数 (默认: 1)')
    parser.add_argument('-d', '--delay', type=float, default=2.0, help='页面间延迟时间(秒) (默认: 2.0)')
    parser.add_argument('--no-headless', action='store_true', help='显示浏览器窗口')
    parser.add_argument('--no-debug', action='store_true', help='不保存调试信息')
    parser.add_argument('--manual', action='store_true', help='遇到登录/验证码时手动解锁，程序等待并继续')
    parser.add_argument('--browser', choices=['chrome'], default='chrome', help='选择浏览器: 仅chrome (驱动自动管理)')
    parser.add_argument('--open-in-default', action='store_true', help='同时在系统默认浏览器中打开搜索页，仅用于人眼查看')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='日志级别')
    
    args = parser.parse_args()
    
    # 设置日志
    logger = setup_logging(args.log_level)
    
    try:
        # 创建爬虫配置
        config = SearchConfig(
            keyword=args.keyword,
            max_pages=args.pages,
            delay_min=args.delay,
            delay_max=args.delay + 1.0,
            headless=not args.no_headless,
            save_debug=not args.no_debug,
            manual_unlock=args.manual,
            browser=args.browser,
            open_in_default=args.open_in_default
        )
        
        logger.info(f"开始爬取Temu搜索: {args.keyword}, 共 {args.pages} 页")
        
        # 使用上下文管理器运行爬虫
        with TemuSpider(config) as spider:
            result = spider.crawl()
            
            # 显示结果
            print_results(result, args.keyword)
            
            # 保存结果
            spider.save_results(result, args.keyword)
            
            # 显示错误信息
            if result.error_messages:
                logger.warning("爬取过程中出现以下错误:")
                for error in result.error_messages:
                    logger.warning(f"  - {error}")
        
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
        sys.exit(1)


def print_results(result, keyword: str):
    """打印爬取结果"""
    print(f"\n{'='*50}")
    print(f"Temu爬取结果 - 关键词: {keyword}")
    print(f"{'='*50}")
    print(f"总产品数: {result.total_count}")
    print(f"成功页数: {result.success_pages}")
    print(f"失败页数: {result.failed_pages}")
    
    if result.products:
        print(f"\n前5个产品示例:")
        print("-" * 50)
        for i, product in enumerate(result.products[:5], 1):
            print(f"{i}. {product.title}")
            print(f"   价格: {product.price}")
            if product.original_price:
                print(f"   原价: {product.original_price}")
            if product.discount:
                print(f"   折扣: {product.discount}")
            if product.rating:
                print(f"   评分: {product.rating}")
            if product.sales_count:
                print(f"   销量: {product.sales_count}")
            print(f"   链接: {product.product_url}")
            print()
    else:
        print("\n未获取到任何产品信息")
        print("请检查:")
        print("1. 网络连接是否正常")
        print("2. 关键词是否正确")
        print("3. 是否被反爬虫系统拦截")
        print("4. 查看调试文件了解更多信息")


def run_simple_crawl(keyword: str, max_pages: int = 1) -> List[dict]:
    """简单的爬取函数，返回产品数据"""
    config = SearchConfig(
        keyword=keyword,
        max_pages=max_pages,
        headless=True,
        save_debug=True
    )
    
    with TemuSpider(config) as spider:
        result = spider.crawl()
        spider.save_results(result, keyword)
        return [product.to_dict() for product in result.products]


if __name__ == "__main__":
    main()
