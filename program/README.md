# 跨境电商选品系统

一个基于数据驱动的智能选品平台，帮助跨境电商发现市场机会，优化产品策略。

## 🏗️ 项目架构

```
program/
├── frontend/                    # 前端模块 (Vue.js)
│   └── vue-app/                # Vue.js 前端应用
├── backend/                    # 后端模块 (Spring Boot)
│   └── Spring Boot 应用
├── algorithm/                  # 算法模块 (Python)
│   ├── recommender/            # 推荐算法
│   ├── data_processing/        # 数据处理
│   └── model/                 # 机器学习模型
├── crawler/                   # 爬虫模块 (Python)
│   ├── spiders/               # 爬虫脚本
│   └── pipelines/            # 数据处理管道
├── database/                  # 数据库模块
│   ├── schema/               # 数据库结构
│   └── migrations/           # 数据库迁移
└── docs/                     # 项目文档
```

## 🚀 快速开始

### 环境要求

- Java 17+
- Node.js 16+
- Python 3.8+
- PostgreSQL 12+
- Docker & Docker Compose

### 1. 启动所有服务

```bash
# 启动所有服务
./start.sh

# 或者使用Docker Compose
docker-compose up -d
```

### 2. 手动启动各模块

```bash
# 启动后端
cd backend && mvn spring-boot:run

# 启动前端
cd frontend/vue-app && npm run dev

# 启动算法服务
cd algorithm && python main.py

# 启动爬虫服务
cd crawler && python run_spiders.py
```

## 📊 服务端口

| 服务 | 端口 | 描述 |
|------|------|------|
| 前端 | 5000 | Vue.js 应用 |
| 后端 | 8081 | Spring Boot API |
| 算法 | 8082 | 算法服务 |
| 数据库 | 5432 | PostgreSQL |
| Redis | 6379 | 缓存服务 |

## 🔧 技术栈

### 前端
- Vue 3 + Composition API
- Element Plus UI组件
- Pinia 状态管理
- Axios HTTP客户端
- ECharts 数据可视化

### 后端
- Spring Boot 3.4
- Spring Data JPA
- PostgreSQL 数据库
- Lombok 代码简化
- Spring Actuator 监控

### 算法
- Python 3.9+
- Pandas + NumPy 数据处理
- Scikit-learn 机器学习
- PyTorch 深度学习
- FastAPI 服务框架

### 爬虫
- Scrapy 爬虫框架
- Selenium 浏览器自动化
- BeautifulSoup HTML解析
- PostgreSQL 数据存储

## 📈 功能特性

### 🛍️ 商品管理
- 商品信息CRUD
- 价格监控
- 库存管理
- 分类管理

### 🕷️ 数据爬取
- 多平台数据爬取
- 自动化任务调度
- 反爬虫策略
- 数据清洗

### 📊 数据分析
- 智能数据分析
- 可视化图表
- 市场趋势预测
- 商品推荐

### 🤖 推荐算法
- 协同过滤推荐
- 内容推荐
- 混合推荐
- 实时推荐

## 🔒 安全配置

- 数据库连接加密
- API访问控制
- CORS跨域配置
- 请求频率限制
- 用户身份验证

## 📝 开发规范

### 代码规范
- 前端：ESLint + Prettier
- 后端：Checkstyle + SpotBugs
- Python：Black + Flake8
- 数据库：命名规范

### Git规范
- 主分支：main
- 开发分支：develop
- 功能分支：feature/*
- 修复分支：hotfix/*

## 🐳 部署方案

### 开发环境
- Docker Compose本地部署
- 热重载开发模式
- 本地数据库

### 生产环境
- Kubernetes集群
- 负载均衡
- 监控告警
- 日志收集

## 📞 技术支持

- 项目文档：`docs/` 目录
- API文档：`http://localhost:8081/swagger-ui.html`
- 健康检查：`http://localhost:8081/actuator/health`
- 日志查看：`docker-compose logs -f`

---

**注意**: 这是一个完整的项目架构，包含了前后端分离、微服务架构、容器化部署等现代软件开发的最佳实践。
