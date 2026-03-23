#!/usr/bin/env python3
"""
Temu爬虫启动脚本
简化运行方式，不需要设置PYTHONPATH
"""
import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

if __name__ == "__main__":
    # 若带参数，沿用命令行模式；否则进入交互式直跑模式
    if len(sys.argv) > 1:
        from scripts.main import main
        main()
    else:
        # 交互式直跑：不需要系统指令即可开始抓取
        print("Temu 爬虫 - 交互式运行模式")
        try:
            from core.models import SearchConfig
            from spider.temu_spider import TemuSpider
        except Exception as e:
            print(f"导入模块失败: {e}")
            sys.exit(1)

        try:
            keyword = input("请输入搜索关键词（例如: 手机配件）：").strip() or "手机配件"
            pages_in = input("请输入爬取页数（默认1）：").strip()
            pages = int(pages_in) if pages_in.isdigit() and int(pages_in) > 0 else 1

            # 默认展示浏览器窗口，便于人工解锁；保存调试信息
            config = SearchConfig(
                keyword=keyword,
                max_pages=pages,
                delay_min=2.0,
                delay_max=5.0,
                headless=False,
                save_debug=True,
                manual_unlock=True,
                open_in_default=False
            )

            print(f"开始爬取：关键词='{config.keyword}', 页数={config.max_pages}")
            with TemuSpider(config) as spider:
                result = spider.crawl()
                spider.save_results(result, config.keyword)
            print("任务完成。")
        except KeyboardInterrupt:
            print("用户取消。")
        except Exception as e:
            print(f"运行失败: {e}")
