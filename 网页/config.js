/**
 * 跨境电商选品系统 - 配置文件
 * 管理所有系统配置项
 */

// API配置
const API_CONFIG = {
    // 基础URL
    BASE_URL: 'http://localhost:5000/api',
    
    // 数据库API
    DATABASE_API: 'http://localhost:5002/api',
    
    // 分析API
    ANALYSIS_API: 'http://localhost:5003/api',
    
    // 请求超时时间（毫秒）
    TIMEOUT: 30000,
    
    // 重试次数
    RETRY_COUNT: 3
};

// 系统配置
const SYSTEM_CONFIG = {
    // 应用名称
    APP_NAME: '跨境电商选品系统',
    
    // 版本号
    VERSION: '1.0.0',
    
    // 环境
    ENVIRONMENT: 'development', // development, production
    
    // 调试模式
    DEBUG: true,
    
    // 日志级别
    LOG_LEVEL: 'info' // debug, info, warn, error
};

// 数据库配置
const DATABASE_CONFIG = {
    // 主机
    HOST: 'localhost',
    
    // 端口
    PORT: 5432,
    
    // 数据库名
    DATABASE: 'ecommerce_db',
    
    // 用户名
    USER: 'postgres',
    
    // 密码
    PASSWORD: 'password',
    
    // 连接池配置
    POOL: {
        MIN: 2,
        MAX: 10,
        IDLE: 10000
    }
};

// 爬虫配置
const CRAWLER_CONFIG = {
    // 最大页数
    MAX_PAGES: 10,
    
    // 请求延迟（秒）
    DELAY: 2,
    
    // 用户代理
    USER_AGENT: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    
    // 代理列表
    PROXY_LIST: [],
    
    // 重试次数
    RETRY_COUNT: 3,
    
    // 超时时间（秒）
    TIMEOUT: 30
};

// 分析配置
const ANALYSIS_CONFIG = {
    // 分析算法
    ALGORITHM: 'ml', // ml, statistical, hybrid
    
    // 预测模型
    PREDICTION_MODEL: 'linear_regression',
    
    // 特征工程
    FEATURE_ENGINEERING: {
        ENABLED: true,
        FEATURES: ['price', 'rating', 'sales', 'category', 'brand']
    },
    
    // 可视化配置
    VISUALIZATION: {
        CHART_TYPE: 'chart.js', // chart.js, echarts, d3
        THEME: 'default',
        COLORS: ['#667eea', '#764ba2', '#f093fb', '#f5576c']
    }
};

// UI配置
const UI_CONFIG = {
    // 主题
    THEME: {
        PRIMARY_COLOR: '#667eea',
        SECONDARY_COLOR: '#764ba2',
        SUCCESS_COLOR: '#27ae60',
        WARNING_COLOR: '#f39c12',
        DANGER_COLOR: '#e74c3c',
        INFO_COLOR: '#3498db'
    },
    
    // 布局
    LAYOUT: {
        SIDEBAR_WIDTH: 260,
        SIDEBAR_COLLAPSED_WIDTH: 60,
        HEADER_HEIGHT: 60,
        FOOTER_HEIGHT: 40
    },
    
    // 动画
    ANIMATION: {
        DURATION: 300,
        EASING: 'ease-in-out'
    },
    
    // 分页
    PAGINATION: {
        PAGE_SIZE: 20,
        SHOW_SIZE_CHANGER: true,
        SHOW_QUICK_JUMPER: true
    }
};

// 安全配置
const SECURITY_CONFIG = {
    // CORS配置
    CORS: {
        ORIGIN: ['http://localhost:3000', 'http://localhost:5000'],
        CREDENTIALS: true
    },
    
    // 认证
    AUTH: {
        ENABLED: false,
        JWT_SECRET: 'your-secret-key',
        TOKEN_EXPIRE: 3600 // 秒
    },
    
    // 限流
    RATE_LIMIT: {
        ENABLED: true,
        WINDOW_MS: 900000, // 15分钟
        MAX: 100 // 最大请求数
    }
};

// 日志配置
const LOG_CONFIG = {
    // 日志级别
    LEVEL: 'info',
    
    // 日志文件
    FILES: {
        ACCESS: 'logs/access.log',
        ERROR: 'logs/error.log',
        APPLICATION: 'logs/app.log'
    },
    
    // 日志格式
    FORMAT: 'combined',
    
    // 日志轮转
    ROTATION: {
        ENABLED: true,
        MAX_SIZE: '10MB',
        MAX_FILES: 5
    }
};

// 缓存配置
const CACHE_CONFIG = {
    // Redis配置
    REDIS: {
        HOST: 'localhost',
        PORT: 6379,
        PASSWORD: '',
        DB: 0
    },
    
    // 缓存策略
    STRATEGY: {
        TTL: 3600, // 秒
        MAX_KEYS: 1000,
        ENABLED: true
    }
};

// 监控配置
const MONITORING_CONFIG = {
    // 健康检查
    HEALTH_CHECK: {
        ENABLED: true,
        INTERVAL: 30000, // 毫秒
        ENDPOINTS: ['/api/health', '/api/stats']
    },
    
    // 性能监控
    PERFORMANCE: {
        ENABLED: true,
        METRICS: ['response_time', 'throughput', 'error_rate']
    },
    
    // 告警
    ALERTS: {
        ENABLED: true,
        CHANNELS: ['email', 'webhook'],
        THRESHOLDS: {
            ERROR_RATE: 0.05,
            RESPONSE_TIME: 5000
        }
    }
};

// 导出配置
if (typeof module !== 'undefined' && module.exports) {
    // Node.js环境
    module.exports = {
        API_CONFIG,
        SYSTEM_CONFIG,
        DATABASE_CONFIG,
        CRAWLER_CONFIG,
        ANALYSIS_CONFIG,
        UI_CONFIG,
        SECURITY_CONFIG,
        LOG_CONFIG,
        CACHE_CONFIG,
        MONITORING_CONFIG
    };
} else {
    // 浏览器环境
    window.CONFIG = {
        API_CONFIG,
        SYSTEM_CONFIG,
        DATABASE_CONFIG,
        CRAWLER_CONFIG,
        ANALYSIS_CONFIG,
        UI_CONFIG,
        SECURITY_CONFIG,
        LOG_CONFIG,
        CACHE_CONFIG,
        MONITORING_CONFIG
    };
}
