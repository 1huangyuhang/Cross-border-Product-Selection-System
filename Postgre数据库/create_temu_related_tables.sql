-- 0.商品基础信息表（temu_product_base）
CREATE TABLE temu_product_base (
    id SERIAL PRIMARY KEY,  -- 自增主键（数据库内部用）
    item_id VARCHAR(50) NOT NULL,  -- TEMU商品唯一ID（业务键）
    platform VARCHAR(20) NOT NULL DEFAULT 'temu',
    title VARCHAR(200) NOT NULL,  -- 商品标题
    main_image_url VARCHAR(255),  -- 主图URL
    sku VARCHAR(50),  -- 商品规格编码
    category_id INT NOT NULL,  -- 品类ID（关联temu_category表）
    category_path VARCHAR(100) NOT NULL,  -- 冗余品类路径（如"数码-手机配件"，减少JOIN）
    delivery_mode VARCHAR(20) NOT NULL,  -- 发货模式（自发货/仓发）
    drainage_tags TEXT[],  -- 引流标签（9.9元/秒杀等）
    is_subsidy BOOLEAN DEFAULT FALSE,  -- 是否平台补贴品
    weight DECIMAL(10,2),  -- 重量（kg）
    volume DECIMAL(10,2),  -- 体积（m³）
    ext_info JSONB,  -- 预留扩展字段（新增属性无需改表）
    first_crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 首次爬取时间
    last_crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 最后更新时间
    UNIQUE(item_id)  -- 确保item_id唯一
);

-- 创建索引：item_id（关联查询用）
CREATE INDEX idx_temu_product_base_item_id ON temu_product_base(item_id);

-- 创建索引：category_id（按品类筛选用）
CREATE INDEX idx_temu_product_base_category_id ON temu_product_base(category_id);

-- 1.品类配置表（temu_category）
CREATE TABLE temu_category (
    id SERIAL PRIMARY KEY,  -- 品类ID（自增，供product_base关联）
    category_name VARCHAR(50) NOT NULL UNIQUE,  -- 品类名称（如"手机配件"）
    category_path VARCHAR(100) NOT NULL UNIQUE,  -- 品类路径（如"数码-手机配件"）
    commission_rate DECIMAL(5,2) NOT NULL,  -- 品类佣金率（如10%）
    audit_requirements TEXT[],  -- 品类审核要求（如"需质检报告"）
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP  -- 配置更新时间
);

-- 索引：category_path（快速查询品类路径对应的佣金率）
CREATE INDEX idx_temu_category_path ON temu_category(category_path);

-- 2.市场需求数据表（temu_product_demand）
CREATE TABLE temu_product_demand (
    id SERIAL PRIMARY KEY,
    item_id VARCHAR(50) NOT NULL,  -- 关联商品基础表
    platform VARCHAR(20) NOT NULL DEFAULT 'temu',
    sales_7d INT NOT NULL,  -- 近7天销量（TEMU爆品核心指标）
    sold_count INT NOT NULL,  -- 累计已售件数
    collect_count INT DEFAULT 0,  -- 收藏量
    live_mount_count INT DEFAULT 0,  -- 直播间挂载次数
    hot_rank INT,  -- 品类热卖榜排名
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 爬取时间
    ext_info JSONB,  -- 预留扩展字段（如"搜索量"）
    -- 外键关联（删除商品时，级联删除需求数据）
    CONSTRAINT fk_demand_item_id FOREIGN KEY (item_id)
        REFERENCES temu_product_base(item_id) ON DELETE CASCADE
);

-- 复合索引：先按item_id，再按crawl_time（支持"查某商品的历史销量趋势"）
CREATE INDEX idx_temu_demand_item_crawl ON temu_product_demand(item_id, crawl_time);
-- 单索引：crawl_time（支持"查某天的全品类销量"）
CREATE INDEX idx_temu_demand_crawl_time ON temu_product_demand(crawl_time);

-- 3.产品竞争力数据表（temu_product_competition）
CREATE TABLE temu_product_competition (
    id SERIAL PRIMARY KEY,
    item_id VARCHAR(50) NOT NULL,
    platform VARCHAR(20) NOT NULL DEFAULT 'temu',
    same_price_competitor_count INT NOT NULL,  -- 同价位竞品数
    top5_sales_ratio DECIMAL(5,2),  -- TOP5卖家销量占比
    competitor_avg_subsidy DECIMAL(10,2),  -- 竞品平均补贴金额
    competitor_avg_rating DECIMAL(3,2),  -- 竞品平均评分
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ext_info JSONB,  -- 预留扩展字段（如"竞品价格分布"）
    CONSTRAINT fk_competition_item_id FOREIGN KEY (item_id)
        REFERENCES temu_product_base(item_id) ON DELETE CASCADE
);

-- 索引：item_id + crawl_time（查询某商品的竞争趋势）
CREATE INDEX idx_temu_competition_item_crawl ON temu_product_competition(item_id, crawl_time);

-- 4.价格 & 利润数据表（temu_product_profit）
CREATE TABLE temu_product_profit (
    id SERIAL PRIMARY KEY,
    item_id VARCHAR(50) NOT NULL,
    platform VARCHAR(20) NOT NULL DEFAULT 'temu',
    category_id INT NOT NULL,  -- 冗余品类ID（关联temu_category）
    commission_rate DECIMAL(5,2) NOT NULL,  -- 冗余佣金率（避免JOIN，高频查询用）
    original_price DECIMAL(10,2) NOT NULL,  -- 原价
    subsidy_price DECIMAL(10,2) NOT NULL,  -- 补贴后售价
    platform_subsidy DECIMAL(10,2) GENERATED ALWAYS AS
        (original_price - subsidy_price) STORED,  -- 平台补贴金额
    purchase_cost DECIMAL(10,2) NOT NULL,  -- 采购成本（人民币）
    logistics_cost DECIMAL(10,2) NOT NULL,  -- 物流成本（人民币）
    return_rate DECIMAL(5,2) NOT NULL DEFAULT 0.08,  -- 退货率（TEMU平均值）
    return_loss DECIMAL(10,2) GENERATED ALWAYS AS
        ((purchase_cost + logistics_cost) * return_rate) STORED,  -- 退货损失
    profit DECIMAL(10,2) GENERATED ALWAYS AS  -- 利润（人民币）
        (subsidy_price * 6.9 - purchase_cost - logistics_cost
        - (subsidy_price * 6.9 * commission_rate / 100) - ((purchase_cost + logistics_cost) * return_rate)) STORED,
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ext_info JSONB,  -- 预留扩展字段（如"关税"）
    CONSTRAINT fk_profit_item_id FOREIGN KEY (item_id)
        REFERENCES temu_product_base(item_id) ON DELETE CASCADE
);

-- 索引：item_id + crawl_time（查利润趋势）、profit（筛选高利润商品）
CREATE INDEX idx_temu_profit_item_crawl ON temu_product_profit(item_id, crawl_time);
CREATE INDEX idx_temu_profit_value ON temu_product_profit(profit);

-- 5.买家反馈数据表（temu_product_feedback）
CREATE TABLE temu_product_feedback (
    id SERIAL PRIMARY KEY,
    item_id VARCHAR(50) NOT NULL,
    platform VARCHAR(20) NOT NULL DEFAULT 'temu',
    rating DECIMAL(3,2) NOT NULL,  -- 商品评分（1-5星）
    review_count INT NOT NULL,  -- 总评论数
    review_count_1star INT NOT NULL DEFAULT 0,
    review_count_2star INT NOT NULL DEFAULT 0,
    review_count_3star INT NOT NULL DEFAULT 0,
    review_count_4star INT NOT NULL DEFAULT 0,
    review_count_5star INT NOT NULL DEFAULT 0,
    negative_review_rate DECIMAL(5,2) GENERATED ALWAYS AS  -- 差评率
        ((review_count_1star + review_count_2star + review_count_3star)::DECIMAL / review_count) STORED,
    logistics_negative_count INT DEFAULT 0,  -- 物流相关差评数
    logistics_negative_ratio DECIMAL(5,2) GENERATED ALWAYS AS  -- 物流差评占比
        (CASE WHEN review_count_1star + review_count_2star + review_count_3star = 0
              THEN 0
              ELSE logistics_negative_count::DECIMAL / (review_count_1star + review_count_2star + review_count_3star)
         END) STORED,
    negative_keywords TEXT[],  -- 差评关键词
    repurchase_rate DECIMAL(5,2) DEFAULT 0.03,  -- 复购率
    crawl_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ext_info JSONB,  -- 预留扩展字段（如"好评关键词"）
    CONSTRAINT fk_feedback_item_id FOREIGN KEY (item_id)
        REFERENCES temu_product_base(item_id) ON DELETE CASCADE
);

-- 索引：item_id + crawl_time（查反馈趋势）、negative_review_rate（筛低差评商品）
CREATE INDEX idx_temu_feedback_item_crawl ON temu_product_feedback(item_id, crawl_time);
CREATE INDEX idx_temu_feedback_negative_rate ON temu_product_feedback(negative_review_rate);