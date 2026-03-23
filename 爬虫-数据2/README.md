# 🕷️ TEMU跨境电商选品爬虫系统

## 📖 项目简介

这是一个专为TEMU跨境电商平台设计的智能爬虫系统，具备强大的反检测能力、网页审查功能和自动搜索能力。系统采用模块化设计，支持多种爬取模式，能够有效应对现代电商网站的反爬虫机制。

## ✨ 核心特性

### 🔍 智能网页审查
- **自动检测商品数据**：智能识别页面是否正常显示商品信息
- **验证码识别**：自动检测各种验证码和安全验证机制
- **反爬系统检测**：识别并处理网站的反爬虫拦截
- **搜索结果验证**：确保搜索结果的有效性和完整性

### 🔄 自动搜索功能
- **智能搜索框定位**：自动识别页面中的搜索输入框
- **人类行为模拟**：逐字符输入，模拟真实用户操作
- **自动搜索执行**：智能点击搜索按钮或执行搜索操作
- **搜索状态验证**：确认搜索是否成功执行

### 🛡️ 高级反爬检测
- **多策略处理**：等待冷却、清除缓存、更换User-Agent、模拟人类行为
- **智能重试机制**：自动尝试多种解决方案
- **失败处理**：无法解决时给出明确提示并安全终止

### 👤 用户友好界面
- **交互式输入**：支持用户自定义搜索关键词和页数
- **实时进度显示**：显示爬取进度和状态信息
- **详细错误提示**：提供清晰的错误信息和解决建议

## 🏗️ 项目结构

```
爬虫-数据2/
├── 🚀 主启动文件
│   ├── run_crawler.py          # 主启动入口（推荐）
│   └── enhanced_crawler.py     # 增强版爬虫（核心功能）
│
├── 🧪 测试文件
│   └── test_enhanced_crawler.py # 非交互式测试脚本
│
├── 📂 核心模块 (core/)
│   ├── undetected_driver.py    # 反检测浏览器驱动
│   ├── smart_behavior.py      # 智能行为模拟
│   ├── proxy_pool.py          # 代理IP池管理
│   ├── ml_detection.py        # 机器学习反检测
│   ├── data_validation.py     # 数据验证和清洗
│   ├── real_time_updater.py   # 实时数据更新
│   └── distributed_crawler.py # 分布式爬虫
│
├── 🕷️ 爬虫模块 (crawlers/)
│   └── unified_temu_crawler.py # 统一爬虫类
│
├── 🛠️ 工具模块 (utils/)
│   └── account_recovery_system.py # 账号恢复系统
│
├── 📊 数据目录
│   ├── results/               # 爬取结果存储
│   ├── data/                  # 数据文件存储
│   └── logs/                  # 日志文件
│
├── 🧪 测试目录
│   └── tests/                 # 测试文件
│
├── 📚 文档目录
│   └── docs/                  # 项目文档
│
└── 📋 配置文件
    ├── requirements.txt         # 依赖包列表
    └── README.md            # 项目说明文档
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Chrome浏览器（最新版本）
- 稳定的网络连接

### 安装依赖
```bash
pip install -r requirements.txt
```

### 使用方法

#### 1. 主启动入口（推荐）
```bash
python main.py
```
统一启动入口，支持交互式和命令行模式

#### 2. 改进版爬虫（最新）
```bash
python improved_crawler.py
```
集成所有优化功能：配置管理、日志系统、反检测机制

#### 3. 自动爬虫
```bash
python auto_crawler.py
```
完全非交互式，自动运行爬虫

#### 4. 增强版爬虫
```bash
python enhanced_crawler.py
```
按提示输入搜索关键词和页数

#### 5. 测试模式
```bash
python test_enhanced_crawler.py
```
功能验证和调试

## 📋 功能对比

| 功能特性 | 增强版爬虫 | 测试脚本 |
|----------|------------|----------|
| 网页审查 | ✅ | ✅ |
| 自动搜索 | ✅ | ✅ |
| 反爬检测 | ✅ | ✅ |
| 用户交互 | ✅ | ❌ |
| 数据质量分析 | ✅ | ✅ |
| 错误处理 | ✅ | ✅ |
| 日志记录 | ✅ | ✅ |

## 🔧 核心功能详解

### 1. 网页审查系统
```python
def inspect_page_content(self, url: str) -> Tuple[bool, str]:
    """
    智能网页审查功能
    - 检测页面标题和内容
    - 识别验证码和安全验证
    - 检测反爬系统拦截
    - 验证商品元素存在性
    """
```

### 2. 自动搜索系统
```python
def auto_search_product(self, keyword: str) -> bool:
    """
    智能自动搜索功能
    - 多选择器搜索框定位
    - 人类行为模拟输入
    - 智能搜索执行
    - 搜索结果验证
    """
```

### 3. 反爬检测处理
```python
def handle_anti_bot_detection(self) -> bool:
    """
    高级反爬系统处理
    - 等待冷却期
    - 清除浏览器数据
    - 更换User-Agent
    - 模拟人类行为
    """
```

## 📊 数据输出

### 商品信息结构
```json
{
  "title": "商品标题",
  "price": "价格信息",
  "discount": "折扣信息",
  "rating": "评分信息",
  "link": "商品链接",
  "image": "商品图片"
}
```

### 数据质量分析
- **总商品数**：爬取的商品总数
- **有效标题**：有效标题的百分比
- **有效价格**：有效价格的百分比
- **有效链接**：有效链接的百分比
- **整体质量**：综合质量评分

## 🛠️ 高级配置

### 代理设置
```python
# 在 enhanced_crawler.py 中配置代理
proxy_config = {
    "http": "http://proxy-server:port",
    "https": "https://proxy-server:port"
}
```

### 反检测设置
```python
# 自定义反检测参数
crawler = EnhancedTemuCrawler()
crawler.max_retry_attempts = 5  # 最大重试次数
crawler.search_timeout = 30     # 搜索超时时间
crawler.page_load_timeout = 20  # 页面加载超时
```

## 📈 性能优化

### 1. 浏览器优化
- 禁用图片加载（提高速度）
- 禁用不必要的插件
- 优化窗口大小设置

### 2. 网络优化
- 智能重试机制
- 请求间隔控制
- 代理IP轮换

### 3. 数据处理优化
- 实时数据验证
- 智能去重
- 批量处理

## 🔍 故障排除

### 常见问题

#### 1. 浏览器驱动问题
```bash
# 更新Chrome浏览器到最新版本
# 检查ChromeDriver版本兼容性
```

#### 2. 网络连接问题
```bash
# 检查网络连接
# 尝试使用代理服务器
```

#### 3. 反爬检测问题
```bash
# 降低爬取频率
# 使用代理IP
# 手动完成验证码
```

### 日志分析
查看 `logs/` 目录下的日志文件，分析具体的错误信息。

## 📝 使用示例

### 基本使用
```python
from enhanced_crawler import EnhancedTemuCrawler

# 创建爬虫实例
crawler = EnhancedTemuCrawler()

# 爬取商品
products = crawler.crawl_products("手机配件", 3)

# 处理结果
for product in products:
    print(f"标题: {product['title']}")
    print(f"价格: {product['price']}")
```

### 高级配置
```python
# 自定义配置
crawler = EnhancedTemuCrawler()
crawler.max_retry_attempts = 5
crawler.search_timeout = 60
crawler.page_load_timeout = 30

# 开始爬取
products = crawler.crawl_products("耳机", 5)
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持与反馈

如果您在使用过程中遇到问题或有改进建议，请：

1. 查看故障排除部分
2. 检查日志文件
3. 提交 Issue
4. 联系开发团队

## 🎯 未来计划

- [ ] 支持更多电商平台
- [ ] 增加数据可视化功能
- [ ] 优化反检测算法
- [ ] 添加机器学习模型
- [ ] 支持分布式部署

---

**注意**：请遵守相关网站的使用条款和robots.txt文件，合理使用爬虫工具，避免对目标网站造成过大负担。