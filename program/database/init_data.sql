-- 跨境电商选品系统 - 初始化数据
-- 按照software.md文档要求实现数据持久化

-- 插入示例商品数据
INSERT INTO products (title, price, original_price, rating, review_count, sales_count, image_url, product_url, category, brand, description, keywords, platform, platform_id, is_available, crawl_date, created_at, updated_at) VALUES
('无线蓝牙耳机', 199.99, 299.99, 4.5, 1250, 8900, 'https://via.placeholder.com/300x300', 'https://temu.com/product/123', '电子产品', 'Apple', '高品质无线蓝牙耳机，降噪功能强大', '耳机,蓝牙,降噪,音乐', 'temu', 'temu_123', true, NOW(), NOW(), NOW()),
('智能手表', 599.99, 799.99, 4.7, 890, 5600, 'https://via.placeholder.com/300x300', 'https://temu.com/product/124', '电子产品', 'Samsung', '多功能智能手表，健康监测', '手表,智能,健康,运动', 'temu', 'temu_124', true, NOW(), NOW(), NOW()),
('便携充电宝', 89.99, 129.99, 4.3, 2100, 12000, 'https://via.placeholder.com/300x300', 'https://temu.com/product/125', '电子产品', 'Anker', '大容量便携充电宝，快充技术', '充电宝,便携,快充,移动电源', 'temu', 'temu_125', true, NOW(), NOW(), NOW()),
('时尚T恤', 29.99, 49.99, 4.2, 450, 3200, 'https://via.placeholder.com/300x300', 'https://temu.com/product/126', '服装', 'Nike', '舒适棉质T恤，多种颜色可选', 'T恤,服装,时尚,棉质', 'temu', 'temu_126', true, NOW(), NOW(), NOW()),
('运动鞋', 159.99, 199.99, 4.6, 680, 4500, 'https://via.placeholder.com/300x300', 'https://temu.com/product/127', '服装', 'Adidas', '专业运动鞋，透气舒适', '运动鞋,运动,舒适,透气', 'temu', 'temu_127', true, NOW(), NOW(), NOW()),
('咖啡机', 299.99, 399.99, 4.4, 320, 1800, 'https://via.placeholder.com/300x300', 'https://temu.com/product/128', '家居用品', 'Philips', '全自动咖啡机，多种咖啡模式', '咖啡机,家居,自动,咖啡', 'temu', 'temu_128', true, NOW(), NOW(), NOW()),
('蓝牙音箱', 79.99, 119.99, 4.1, 890, 5200, 'https://via.placeholder.com/300x300', 'https://temu.com/product/129', '电子产品', 'JBL', '便携蓝牙音箱，音质清晰', '音箱,蓝牙,便携,音乐', 'temu', 'temu_129', true, NOW(), NOW(), NOW()),
('保温杯', 39.99, 59.99, 4.5, 1200, 8500, 'https://via.placeholder.com/300x300', 'https://temu.com/product/130', '家居用品', 'Thermos', '不锈钢保温杯，24小时保温', '保温杯,不锈钢,保温,便携', 'temu', 'temu_130', true, NOW(), NOW(), NOW());

-- 插入示例用户数据
INSERT INTO users (username, email, created_at, updated_at) VALUES
('user001', 'user001@example.com', NOW(), NOW()),
('user002', 'user002@example.com', NOW(), NOW()),
('user003', 'user003@example.com', NOW(), NOW()),
('user004', 'user004@example.com', NOW(), NOW()),
('user005', 'user005@example.com', NOW(), NOW());

-- 插入示例用户交互数据
INSERT INTO user_interactions (user_id, product_id, interaction_type, rating, created_date) VALUES
(1, 1, 'view', NULL, NOW() - INTERVAL '1 day'),
(1, 2, 'view', NULL, NOW() - INTERVAL '2 hours'),
(1, 3, 'purchase', 5, NOW() - INTERVAL '1 hour'),
(2, 1, 'view', NULL, NOW() - INTERVAL '3 hours'),
(2, 4, 'purchase', 4, NOW() - INTERVAL '30 minutes'),
(3, 2, 'view', NULL, NOW() - INTERVAL '1 hour'),
(3, 5, 'purchase', 5, NOW() - INTERVAL '2 hours'),
(4, 3, 'view', NULL, NOW() - INTERVAL '4 hours'),
(4, 6, 'purchase', 4, NOW() - INTERVAL '1 day'),
(5, 1, 'purchase', 5, NOW() - INTERVAL '2 days'),
(5, 7, 'view', NULL, NOW() - INTERVAL '1 hour'),
(5, 8, 'purchase', 4, NOW() - INTERVAL '3 hours');

-- 创建索引以优化查询性能
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
CREATE INDEX IF NOT EXISTS idx_products_platform ON products(platform);
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);
CREATE INDEX IF NOT EXISTS idx_products_rating ON products(rating);
CREATE INDEX IF NOT EXISTS idx_products_sales_count ON products(sales_count);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);

CREATE INDEX IF NOT EXISTS idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_interactions_product_id ON user_interactions(product_id);
CREATE INDEX IF NOT EXISTS idx_user_interactions_type ON user_interactions(interaction_type);
CREATE INDEX IF NOT EXISTS idx_user_interactions_created_date ON user_interactions(created_date);

-- 创建视图以简化常用查询
CREATE OR REPLACE VIEW product_stats AS
SELECT 
    p.id,
    p.title,
    p.price,
    p.rating,
    p.sales_count,
    p.category,
    p.brand,
    COUNT(ui.id) as interaction_count,
    AVG(ui.rating) as avg_user_rating
FROM products p
LEFT JOIN user_interactions ui ON p.id = ui.product_id
GROUP BY p.id, p.title, p.price, p.rating, p.sales_count, p.category, p.brand;

CREATE OR REPLACE VIEW category_performance AS
SELECT 
    category,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    AVG(rating) as avg_rating,
    SUM(sales_count) as total_sales
FROM products
GROUP BY category
ORDER BY total_sales DESC;

-- 创建存储过程用于推荐算法
CREATE OR REPLACE FUNCTION get_user_recommendations(user_id_param INTEGER, limit_param INTEGER DEFAULT 10)
RETURNS TABLE(
    product_id BIGINT,
    title VARCHAR,
    price DECIMAL,
    rating DECIMAL,
    recommendation_score DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    WITH user_preferences AS (
        SELECT 
            p.category,
            AVG(ui.rating) as avg_rating,
            COUNT(*) as interaction_count
        FROM user_interactions ui
        JOIN products p ON ui.product_id = p.id
        WHERE ui.user_id = user_id_param
        GROUP BY p.category
    ),
    similar_users AS (
        SELECT DISTINCT ui2.user_id
        FROM user_interactions ui1
        JOIN user_interactions ui2 ON ui1.product_id = ui2.product_id
        WHERE ui1.user_id = user_id_param
        AND ui2.user_id != user_id_param
        GROUP BY ui2.user_id
        HAVING COUNT(*) >= 2
    ),
    recommendations AS (
        SELECT 
            p.id as product_id,
            p.title,
            p.price,
            p.rating,
            (p.rating * 0.6 + (p.sales_count / 1000.0) * 0.4) as recommendation_score
        FROM products p
        WHERE p.id NOT IN (
            SELECT product_id 
            FROM user_interactions 
            WHERE user_id = user_id_param
        )
        AND p.is_available = true
    )
    SELECT 
        r.product_id,
        r.title,
        r.price,
        r.rating,
        r.recommendation_score
    FROM recommendations r
    ORDER BY r.recommendation_score DESC
    LIMIT limit_param;
END;
$$ LANGUAGE plpgsql;

-- 创建触发器用于自动更新统计信息
CREATE OR REPLACE FUNCTION update_product_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- 更新商品的交互统计
    UPDATE products 
    SET updated_at = NOW()
    WHERE id = NEW.product_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_product_stats
    AFTER INSERT OR UPDATE ON user_interactions
    FOR EACH ROW
    EXECUTE FUNCTION update_product_stats();

-- 创建定时任务清理过期数据（需要pg_cron扩展）
-- CREATE EXTENSION IF NOT EXISTS pg_cron;
-- SELECT cron.schedule('cleanup-old-data', '0 2 * * *', 'DELETE FROM user_interactions WHERE created_date < NOW() - INTERVAL ''1 year'';');

COMMIT;
