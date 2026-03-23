-- 跨境电商选品系统 - 数据库索引优化
-- 创建时间: 2024-01-01

-- 商品表索引
CREATE INDEX IF NOT EXISTS idx_products_platform ON products(platform);
CREATE INDEX IF NOT EXISTS idx_products_platform_id ON products(platform_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_products_rating ON products(rating);
CREATE INDEX IF NOT EXISTS idx_products_sales_count ON products(sales_count);
CREATE INDEX IF NOT EXISTS idx_products_is_available ON products(is_available);
CREATE INDEX IF NOT EXISTS idx_products_crawl_date ON products(crawl_date);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);

-- 复合索引
CREATE INDEX IF NOT EXISTS idx_products_platform_category ON products(platform, category);
CREATE INDEX IF NOT EXISTS idx_products_category_brand ON products(category, brand);
CREATE INDEX IF NOT EXISTS idx_products_price_rating ON products(price, rating);

-- 全文搜索索引
CREATE INDEX IF NOT EXISTS idx_products_title_gin ON products USING gin(to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_products_keywords_gin ON products USING gin(to_tsvector('english', keywords));

-- 爬虫任务表索引
CREATE INDEX IF NOT EXISTS idx_crawler_tasks_status ON crawler_tasks(status);
CREATE INDEX IF NOT EXISTS idx_crawler_tasks_platform ON crawler_tasks(platform);
CREATE INDEX IF NOT EXISTS idx_crawler_tasks_created_at ON crawler_tasks(created_at);

-- 分析结果表索引
CREATE INDEX IF NOT EXISTS idx_analysis_results_type ON analysis_results(analysis_type);
CREATE INDEX IF NOT EXISTS idx_analysis_results_status ON analysis_results(status);
CREATE INDEX IF NOT EXISTS idx_analysis_results_created_at ON analysis_results(created_at);

-- 用户表索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- 用户收藏表索引
CREATE INDEX IF NOT EXISTS idx_user_favorites_user_id ON user_favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_user_favorites_product_id ON user_favorites(product_id);

-- 商品评论表索引
CREATE INDEX IF NOT EXISTS idx_product_reviews_product_id ON product_reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_product_reviews_user_id ON product_reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_product_reviews_rating ON product_reviews(rating);
CREATE INDEX IF NOT EXISTS idx_product_reviews_created_at ON product_reviews(created_at);

-- 系统配置表索引
CREATE INDEX IF NOT EXISTS idx_system_config_key ON system_config(config_key);
