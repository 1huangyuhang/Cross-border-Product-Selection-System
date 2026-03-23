# Temu爬虫系统

一个模块化、可维护的Temu产品信息爬虫系统，专门用于爬取Temu网站的产品信息。

## 功能特性

- 🎯 **专注产品信息**: 爬取产品标题、价格、折扣、上架日期、产品链接等关键信息
- 🏗️ **模块化设计**: 代码结构清晰，易于维护和扩展
- 🛡️ **反反爬措施**: 内置多种反检测技术，提高爬取成功率
- 📊 **多格式输出**: 支持JSON和CSV格式保存数据
- 🔧 **灵活配置**: 支持自定义搜索参数和爬取策略
- 📝 **详细日志**: 完整的日志记录和调试信息

## 项目结构

```
数据-爬虫/
├── core/                    # 核心模块
│   ├── models.py           # 数据模型定义
│   ├── utils.py            # 工具函数
│   └── url_generator.py    # URL生成器
├── spider/                 # 爬虫模块
│   ├── base_spider.py      # 基础爬虫类
│   ├── temu_spider.py      # Temu爬虫实现
│   └── temu_parser.py      # Temu页面解析器
├── scripts/                # 脚本模块
│   ├── main.py            # 主程序入口
│   ├── example.py         # 使用示例
│   └── test_urls.py       # URL测试脚本
├── run.py                 # 启动脚本
└── README.md              # 说明文档
```

## 快速开始

### 1. 基础使用

```python
from core.models import SearchConfig
from spider.temu_spider import TemuSpider

# 创建配置
config = SearchConfig(
    keyword="手机配件",
    max_pages=1,
    headless=True
)

# 运行爬虫
with TemuSpider(config) as spider:
    result = spider.crawl()

    # 显示结果
    print(f"获取到 {result.total_count} 个产品")
    for product in result.products:
        print(f"- {product.title}: {product.price}")

    # 保存结果
    spider.save_results(result, config.keyword)
```

### 2. 命令行使用

```bash
# 最简单的运行方式
python run.py "手机配件"

# 或者使用完整的路径
python scripts/main.py "手机配件"

# 爬取多页
python run.py "手机配件" -p 3

# 自定义延迟
python run.py "手机配件" -d 5.0

# 显示浏览器窗口
python run.py "手机配件" --no-headless

# 不保存调试信息
python run.py "手机配件" --no-debug
```

### 3. 高级配置

```python
from core.models import SearchConfig
from spider.temu_spider import TemuSpider

# 自定义配置
config = SearchConfig(
    keyword="蓝牙耳机",
    max_pages=2,           # 爬取2页
    delay_min=1.0,         # 最小延迟1秒
    delay_max=3.0,         # 最大延迟3秒
    headless=False,        # 显示浏览器窗口
    save_debug=True        # 保存调试信息
)

with TemuSpider(config) as spider:
    result = spider.crawl()
    spider.save_results(result, config.keyword)
```

## 数据模型

### TemuProduct
产品信息数据模型，包含以下字段：

- `title`: 产品标题
- `price`: 价格
- `discount`: 折扣信息
- `listing_date`: 上架日期
- `product_url`: 产品链接
- `original_price`: 原价（可选）
- `rating`: 评分（可选）
- `sales_count`: 销量（可选）
- `image_url`: 图片链接（可选）
- `category`: 分类（可选）

### SearchConfig
搜索配置模型：

- `keyword`: 搜索关键词
- `max_pages`: 最大页数
- `delay_min`: 最小延迟时间
- `delay_max`: 最大延迟时间
- `headless`: 是否无头模式
- `save_debug`: 是否保存调试信息

## 输出文件

爬虫会在 `temu_debug` 目录下生成以下文件：

- `temu_{keyword}_products_{timestamp}.json`: JSON格式的产品数据
- `temu_{keyword}_products_{timestamp}.csv`: CSV格式的产品数据
- `temu_{keyword}_summary_{timestamp}.json`: 爬取汇总信息
- `temu_page_debug_{timestamp}.html`: 页面调试信息

## 反反爬措施

系统内置了多种反反爬措施：

1. **随机User-Agent**: 随机选择浏览器标识
2. **人类行为模拟**: 模拟真实用户的浏览行为
3. **随机延迟**: 页面间随机延迟
4. **浏览器指纹伪装**: 隐藏自动化特征
5. **多种访问策略**: 支持不同的访问路径

## 错误处理

系统提供完善的错误处理机制：

- 自动重试机制
- 详细的错误日志
- 调试信息保存
- 优雅的异常处理

## 核心改进

### 🎯 **问题分析**

根据日志分析，发现原爬虫系统存在以下问题：

1. **URL格式错误**: 原系统使用的URL格式与Temu实际搜索页面不匹配
2. **重定向处理**: 被重定向到登录页面后，尝试的绕过URL仍然使用错误格式
3. **反爬检测**: Temu的反爬机制较强，需要更精确的URL策略

### 🔧 **解决方案**

#### 1. **创建URL生成器模块** (`core/url_generator.py`)

基于实际Temu搜索URL格式：
```
https://www.temu.com/search_result.html?search_key=%E6%89%8B%E6%9C%BA%E9%85%8D%E4%BB%B6&search_method=user&refer_page_el_sn=200010&srch_enter_source=top_search_entrance_10005&refer_page_name=home&refer_page_id=10005_1760104053807_yk2qsg2i6v&refer_page_sn=10005&_x_sessn_id=mzftbh1enc
```

**主要功能：**
- 自动生成正确的Temu搜索URL
- 支持URL编码处理
- 生成时间戳和会话ID
- 提供多种URL格式备选

#### 2. **更新爬虫策略** (`spider/temu_spider.py`)

**改进内容：**
- 集成URL生成器
- 使用正确的`search_result.html`格式
- 优化绕过登录重定向的策略
- 改进URL选择逻辑

#### 3. **测试验证** (`scripts/test_urls.py`)

创建测试脚本验证：
- URL生成正确性
- 参数编码/解码
- 多种关键词支持

### 📊 **改进效果**

#### 改进前的问题：
```
❌ 使用错误URL格式: /search?q=keyword
❌ 绕过策略无效: 仍使用错误格式
❌ 被重定向到登录页面
❌ 无法获取产品数据
```

#### 改进后的效果：
```
✅ 使用正确URL格式: /search_result.html?search_key=...
✅ 智能URL生成: 多种格式备选
✅ 正确的参数编码: 支持中文关键词
✅ 优化的绕过策略: 使用正确格式重试
```

## 依赖安装

```bash
pip install selenium beautifulsoup4 webdriver-manager fake-useragent lxml
```

## 注意事项

1. **遵守网站规则**: 请合理使用爬虫，不要对网站造成过大负担
2. **延迟设置**: 建议设置适当的延迟时间，避免被反爬系统拦截
3. **数据准确性**: 网站结构可能变化，需要定期更新解析规则
4. **法律合规**: 请确保爬取行为符合相关法律法规

## 许可证

本项目仅供学习和研究使用，请勿用于商业用途。