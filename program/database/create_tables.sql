-- 跨境电商选品系统 - 数据库表结构
-- 按照software.md文档要求实现PostgreSQL数据库设计

-- 创建数据库（如果不存在）
-- CREATE DATABASE ecommerce_db;

-- 连接到数据库
-- \c ecommerce_db;

-- 1. 商品表 (products)
-- 按照software.md文档要求实现主键/外键/索引
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    price DECIMAL(10,2),
    original_price DECIMAL(10,2),
    rating DECIMAL(2,1) CHECK (rating >= 0 AND rating <= 5),
    review_count INTEGER DEFAULT 0,
    sales_count INTEGER DEFAULT 0,
    url TEXT,
    image_url TEXT,
    description TEXT,
    category VARCHAR(255),
    brand VARCHAR(255),
    keywords TEXT,
    platform VARCHAR(50) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    crawl_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 用户表 (users)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- 3. 用户行为表 (user_interactions)
-- 记录用户与商品的交互行为
CREATE TABLE IF NOT EXISTS user_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    interaction_type VARCHAR(50) NOT NULL, -- 'view', 'click', 'purchase', 'favorite'
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. 爬虫任务表 (crawler_tasks)
-- 记录爬虫执行任务
CREATE TABLE IF NOT EXISTS crawler_tasks (
    id SERIAL PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    keyword VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed'
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    products_crawled INTEGER DEFAULT 0,
    error_message TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. 推荐结果表 (recommendations)
-- 存储推荐算法结果
CREATE TABLE IF NOT EXISTS recommendations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    algorithm_type VARCHAR(50) NOT NULL, -- 'collaborative', 'content', 'hybrid'
    score DECIMAL(5,4) NOT NULL,
    rank_position INTEGER,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. 分析结果表 (analysis_results)
-- 存储数据分析结果
CREATE TABLE IF NOT EXISTS analysis_results (
    id SERIAL PRIMARY KEY,
    analysis_type VARCHAR(100) NOT NULL, -- 'trend_analysis', 'category_analysis', 'price_analysis'
    result_data JSONB,
    summary TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. 商品分类表 (categories)
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INTEGER REFERENCES categories(id),
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. 品牌表 (brands)
CREATE TABLE IF NOT EXISTS brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    logo_url TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引 - 按照software.md文档要求优化索引
-- 商品表索引
CREATE INDEX IF NOT EXISTS idx_products_platform ON products(platform);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_products_rating ON products(rating);
CREATE INDEX IF NOT EXISTS idx_products_created_date ON products(created_date);
CREATE INDEX IF NOT EXISTS idx_products_title_search ON products USING gin(to_tsvector('english', title));

-- 用户交互表索引
CREATE INDEX IF NOT EXISTS idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_interactions_product_id ON user_interactions(product_id);
CREATE INDEX IF NOT EXISTS idx_user_interactions_type ON user_interactions(interaction_type);
CREATE INDEX IF NOT EXISTS idx_user_interactions_created_date ON user_interactions(created_date);

-- 推荐结果表索引
CREATE INDEX IF NOT EXISTS idx_recommendations_user_id ON recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_algorithm_type ON recommendations(algorithm_type);
CREATE INDEX IF NOT EXISTS idx_recommendations_score ON recommendations(score);

-- 爬虫任务表索引
CREATE INDEX IF NOT EXISTS idx_crawler_tasks_status ON crawler_tasks(status);
CREATE INDEX IF NOT EXISTS idx_crawler_tasks_platform ON crawler_tasks(platform);
CREATE INDEX IF NOT EXISTS idx_crawler_tasks_created_date ON crawler_tasks(created_date);

-- 创建触发器 - 自动更新updated_date
CREATE OR REPLACE FUNCTION update_updated_date_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_date = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为products表创建触发器
DROP TRIGGER IF EXISTS update_products_updated_date ON products;
CREATE TRIGGER update_products_updated_date
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_date_column();

-- 为users表创建触发器
DROP TRIGGER IF EXISTS update_users_updated_date ON users;
CREATE TRIGGER update_users_updated_date
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_date_column();

-- 插入初始数据
-- 商品分类数据
INSERT INTO categories (name, description) VALUES
('电子产品', '手机、电脑、数码产品等'),
('服装配饰', '服装、鞋子、包包、配饰等'),
('家居用品', '家具、装饰、厨房用品等'),
('美妆个护', '化妆品、护肤品、个人护理用品等'),
('户外运动', '运动装备、户外用品等')
ON CONFLICT DO NOTHING;

-- 品牌数据
INSERT INTO brands (name, description) VALUES
('Apple', '苹果公司产品'),
('Samsung', '三星电子产品'),
('Nike', '耐克运动品牌'),
('Adidas', '阿迪达斯运动品牌'),
('Uniqlo', '优衣库服装品牌')
ON CONFLICT (name) DO NOTHING;

-- 创建视图 - 商品统计视图
CREATE OR REPLACE VIEW product_statistics AS
SELECT 
    platform,
    category,
    COUNT(*) as total_products,
    AVG(price) as avg_price,
    AVG(rating) as avg_rating,
    SUM(sales_count) as total_sales,
    MAX(created_date) as latest_crawl
FROM products
WHERE is_available = TRUE
GROUP BY platform, category;

-- 创建视图 - 用户推荐视图
CREATE OR REPLACE VIEW user_recommendations AS
SELECT 
    u.id as user_id,
    u.username,
    p.id as product_id,
    p.title,
    p.price,
    p.rating,
    r.score,
    r.algorithm_type,
    r.rank_position
FROM users u
JOIN recommendations r ON u.id = r.user_id
JOIN products p ON r.product_id = p.id
WHERE p.is_available = TRUE
ORDER BY u.id, r.rank_position;

-- 创建存储过程 - 清理过期数据
CREATE OR REPLACE FUNCTION clean_old_data()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    -- 删除30天前的爬虫任务记录
    DELETE FROM crawler_tasks 
    WHERE created_date < CURRENT_TIMESTAMP - INTERVAL '30 days'
    AND status IN ('completed', 'failed');
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    -- 删除90天前的推荐记录
    DELETE FROM recommendations 
    WHERE created_date < CURRENT_TIMESTAMP - INTERVAL '90 days';
    
    GET DIAGNOSTICS deleted_count = deleted_count + ROW_COUNT;
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- 创建存储过程 - 更新商品统计
CREATE OR REPLACE FUNCTION update_product_stats()
RETURNS VOID AS $$
BEGIN
    -- 更新商品的平均评分
    UPDATE products 
    SET rating = (
        SELECT AVG(rating) 
        FROM user_interactions 
        WHERE product_id = products.id 
        AND interaction_type = 'rating'
        AND rating IS NOT NULL
    )
    WHERE id IN (
        SELECT DISTINCT product_id 
        FROM user_interactions 
        WHERE interaction_type = 'rating'
    );
END;
$$ LANGUAGE plpgsql;

-- 创建用户权限
-- 创建应用用户
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'ecommerce_app') THEN
        CREATE ROLE ecommerce_app WITH LOGIN PASSWORD 'app_password';
    END IF;
END
$$;

-- 授予权限
GRANT CONNECT ON DATABASE ecommerce_db TO ecommerce_app;
GRANT USAGE ON SCHEMA public TO ecommerce_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ecommerce_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ecommerce_app;

-- 创建备份脚本注释
-- 按照software.md文档要求实现数据库备份
-- pg_dump -h localhost -U postgres -d ecommerce_db > backup_$(date +%Y%m%d_%H%M%S).sql

-- 创建恢复脚本注释
-- 按照software.md文档要求实现数据库恢复
-- psql -h localhost -U postgres -d ecommerce_db < backup_file.sql

-- 完成数据库初始化
SELECT 'Database initialization completed successfully!' as status;
