package com.project.util;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * 日志工具类
 * 按照software.md文档要求实现日志记录
 */
public class LogUtils {
    
    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    
    /**
     * 记录业务操作日志
     */
    public static void logBusinessOperation(Logger logger, String operation, String details) {
        String timestamp = LocalDateTime.now().format(FORMATTER);
        logger.info("[{}] 业务操作: {} - {}", timestamp, operation, details);
    }
    
    /**
     * 记录API调用日志
     */
    public static void logApiCall(Logger logger, String method, String endpoint, Object request) {
        String timestamp = LocalDateTime.now().format(FORMATTER);
        logger.info("[{}] API调用: {} {} - 请求: {}", timestamp, method, endpoint, request);
    }
    
    /**
     * 记录数据库操作日志
     */
    public static void logDatabaseOperation(Logger logger, String operation, String table, Object data) {
        String timestamp = LocalDateTime.now().format(FORMATTER);
        logger.debug("[{}] 数据库操作: {} 表: {} - 数据: {}", timestamp, operation, table, data);
    }
    
    /**
     * 记录错误日志
     */
    public static void logError(Logger logger, String operation, Exception e) {
        String timestamp = LocalDateTime.now().format(FORMATTER);
        logger.error("[{}] 操作失败: {} - 错误: {}", timestamp, operation, e.getMessage(), e);
    }
    
    /**
     * 记录性能日志
     */
    public static void logPerformance(Logger logger, String operation, long duration) {
        String timestamp = LocalDateTime.now().format(FORMATTER);
        logger.info("[{}] 性能监控: {} - 耗时: {}ms", timestamp, operation, duration);
    }
}
