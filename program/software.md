# 跨境电商数据分析与推荐系统项目文档

## 1. 项目概述
本项目旨在构建一个跨境电商选品及推荐系统，实现前后端分离，功能包括：
- 网络数据爬取、清洗与入库 PostgreSQL。
- 后端 Spring Boot 提供 API 与业务逻辑处理。
- 前端 Vue 或 React 展示页面与数据可视化。
- 推荐算法与数据处理模块进行商品推荐、排序及分析。
- 模块化、可扩展，后续支持 Spring Cloud 微服务架构。

---

## 2. 项目目录结构
project-root/
├── frontend/                
│   └── vue-app/             
│       ├── src/
│       │   ├── components/  
│       │   ├── views/       
│       │   ├── router/      
│       │   ├── store/       
│       │   └── main.js      
│       └── package.json     

├── backend/                 
│   ├── src/main/java/com/project/
│   │   ├── controller/      
│   │   ├── service/         
│   │   ├── repository/      
│   │   └── Application.java
│   └── src/main/resources/application.yml

├── algorithm/               
│   └── recommender.py       

├── crawler/                 
│   └── spiders/             
│       └── product_spider.py

├── database/                
│   └── create_tables.sql    

└── README.md

---

## 3. 技术栈与方法

### 3.1 前端
**技术**：Vue.js / React.js, HTML, CSS, JS, Axios, Pinia/Vuex  

**方法**：
- 组件方法：`setup()`, `mounted()`, `created()`, `emit()`, 全局异常捕获  
- 路由方法：`router.push()`, `router.replace()`, `useRouter()`, `useRoute()`  
- 状态管理：`store.commit()`, `store.dispatch()`, `mapState()`, `mapGetters()`  
- 网络请求：`axios.get()`, `axios.post()`, `axios.put()`, `axios.delete()`, `async/await`, `try/catch`  
- 数据渲染：`map()`, `filter()`, `reduce()`, `v-for`, `v-if`, JSX渲染  

### 3.2 后端
**技术**：Spring Boot, JPA/Hibernate, Scheduler, REST API  

**方法**：
- Controller：`@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@RequestBody`, `@PathVariable`  
- Service：业务逻辑函数、调用算法接口、事务管理  
- Repository：`findById()`, `findAll()`, `save()`, `saveAll()`, `delete()`, `@Query`  
- Scheduler：`@Scheduled` 定时任务  
- 工具方法：日志 `Logger.info/debug/error`, 异常处理 `try/catch`, 数据验证 `StringUtils`, 加密 `BCryptPasswordEncoder`  

### 3.3 数据库
**技术**：PostgreSQL  

**方法**：
- 建表/修改：`CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, 主键/外键/索引  
- 数据操作：`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `JOIN`, `GROUP BY`, `ORDER BY`, 分页查询  
- 事务与连接：`BEGIN`, `COMMIT`, `ROLLBACK`, `session.add()`, `session.commit()`, `cursor.execute()`  

### 3.4 算法模块
**技术**：Python, Pandas, NumPy, Scikit-learn, PyTorch, FastAPI  

**方法**：
- 数据处理：`read_csv()`, `dropna()`, `fillna()`, `array()`, `reshape()`, `StandardScaler.fit_transform()`  
- 推荐算法：`cosine_similarity()`, `NearestNeighbors.fit()`, `TfidfVectorizer.fit_transform()`, 协同过滤, 内容推荐, 混合推荐  
- 模型训练与预测：`model.fit()`, `model.predict()`, `loss.backward()`, `optimizer.step()`, `torch.save()`, `torch.load()`  
- API接口：`FastAPI @app.get`, `@app.post`, JSON返回  

### 3.5 爬虫模块
**技术**：Python, Scrapy, Requests, BeautifulSoup  

**方法**：
- 爬取：`requests.get()`, `response.json()`, Scrapy `start_requests()`, `parse()`, BeautifulSoup `find()`, `select()`  
- 数据清洗：`re.match()`, `re.sub()`, `strip()`, `lower()`, `split()`, `drop_duplicates()`  
- 数据存储：`INSERT INTO`, ORM `session.add()`, `session.commit()`, `executemany()`  
- 调度调用：cron定时、后端 Scheduler 触发、`retry_request()`  

---

## 4. 模块调用与数据流

- **前端 → 后端**：组件调用 Axios → Controller 接收请求 → Service 处理 → Repository 访问数据库  
- **后端 → 数据库**：JPA/SQL 操作 → PostgreSQL  
- **后端 → 算法**：Service 调用算法模块 → 数据处理 → 推荐算法 → 返回结果  
- **Scheduler → 爬虫 → 数据库**：定时任务触发爬虫 → 爬取数据 → 清洗 → 入库  
- **数据库 → 前端**：查询数据 → 返回 JSON → 前端渲染  

---

## 5. 补充设计与优化

- **异常处理**：前端全局捕获，后端 `@ControllerAdvice`  
- **算法持久化**：保存训练模型，支持加载预测  
- **数据库优化**：索引、分页、事务管理  
- **模块化与扩展**：后端支持 Spring Cloud 微服务，算法模块可单独 API 化  

---

## 6. 开发与部署建议

1. 前端和后端分离开发，使用 Docker 或 docker-compose 部署前端、后端和数据库。
2. 使用 Python 虚拟环境管理算法和爬虫依赖。
3. 建立 Git 分支策略，前端/后端/算法/爬虫独立开发，主分支合并。
4. 数据库初始建表及迁移使用 `create_tables.sql` 和 migration 工具（Flyway 或 Alembic）。
5. 项目文档和 API 规范建议维护 `docs/` 目录。