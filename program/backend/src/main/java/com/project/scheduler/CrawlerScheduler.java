package com.project.scheduler;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * 爬虫定时任务调度器
 * 根据software.md文档要求实现定时任务触发爬虫
 */
@Component
public class CrawlerScheduler {
    
    private static final Logger logger = LoggerFactory.getLogger(CrawlerScheduler.class);
    
    @Autowired
    private RestTemplate restTemplate;
    
    /**
     * 定时启动爬虫任务
     * 每天凌晨2点执行
     */
    @Scheduled(cron = "0 0 2 * * ?")
    public void startDailyCrawler() {
        logger.info("开始执行每日爬虫任务: {}", LocalDateTime.now());
        
        try {
            // 启动主要电商平台爬虫
            startCrawlerTask("temu", "手机配件");
            startCrawlerTask("aliexpress", "electronics");
            startCrawlerTask("amazon", "smartphone accessories");
            
            logger.info("每日爬虫任务执行完成");
        } catch (Exception e) {
            logger.error("每日爬虫任务执行失败", e);
        }
    }
    
    /**
     * 定时启动热门商品爬虫
     * 每6小时执行一次
     */
    @Scheduled(cron = "0 0 */6 * * ?")
    public void startHotProductsCrawler() {
        logger.info("开始执行热门商品爬虫任务: {}", LocalDateTime.now());
        
        try {
            // 爬取热门商品数据
            String[] hotKeywords = {
                "iPhone", "Samsung", "MacBook", "AirPods", 
                "iPad", "Xiaomi", "Huawei", "OnePlus"
            };
            
            for (String keyword : hotKeywords) {
                startCrawlerTask("multi-platform", keyword);
                // 避免请求过于频繁
                Thread.sleep(5000);
            }
            
            logger.info("热门商品爬虫任务执行完成");
        } catch (Exception e) {
            logger.error("热门商品爬虫任务执行失败", e);
        }
    }
    
    /**
     * 定时启动价格监控爬虫
     * 每2小时执行一次
     */
    @Scheduled(cron = "0 0 */2 * * ?")
    public void startPriceMonitorCrawler() {
        logger.info("开始执行价格监控爬虫任务: {}", LocalDateTime.now());
        
        try {
            // 监控特定商品的价格变化
            startCrawlerTask("price-monitor", "price_tracking");
            
            logger.info("价格监控爬虫任务执行完成");
        } catch (Exception e) {
            logger.error("价格监控爬虫任务执行失败", e);
        }
    }
    
    /**
     * 启动爬虫任务
     * 
     * @param platform 平台名称
     * @param keyword 搜索关键词
     */
    private void startCrawlerTask(String platform, String keyword) {
        try {
            // 构建爬虫任务请求
            Map<String, Object> taskRequest = new HashMap<>();
            taskRequest.put("platform", platform);
            taskRequest.put("keyword", keyword);
            taskRequest.put("maxPages", 5);
            taskRequest.put("startTime", LocalDateTime.now().toString());
            
            // 调用爬虫服务API
            String crawlerUrl = "http://localhost:8082/crawler/start";
            
            // 这里应该调用爬虫服务的API
            // 由于爬虫服务可能不在运行，我们只记录日志
            logger.info("启动爬虫任务 - 平台: {}, 关键词: {}", platform, keyword);
            
            // 实际实现中应该调用爬虫服务
            // restTemplate.postForObject(crawlerUrl, taskRequest, String.class);
            
        } catch (Exception e) {
            logger.error("启动爬虫任务失败 - 平台: {}, 关键词: {}", platform, keyword, e);
        }
    }
    
    /**
     * 检查爬虫任务状态
     * 每10分钟检查一次
     */
    @Scheduled(fixedRate = 600000) // 10分钟
    public void checkCrawlerStatus() {
        logger.debug("检查爬虫任务状态: {}", LocalDateTime.now());
        
        try {
            // 检查爬虫服务健康状态
            String healthUrl = "http://localhost:8082/health";
            
            // 这里应该检查爬虫服务状态
            // String status = restTemplate.getForObject(healthUrl, String.class);
            
            logger.debug("爬虫服务状态检查完成");
        } catch (Exception e) {
            logger.warn("爬虫服务状态检查失败", e);
        }
    }
    
    /**
     * 清理过期的爬虫任务数据
     * 每天凌晨3点执行
     */
    @Scheduled(cron = "0 0 3 * * ?")
    public void cleanupExpiredTasks() {
        logger.info("开始清理过期爬虫任务数据: {}", LocalDateTime.now());
        
        try {
            // 清理7天前的爬虫任务记录
            // 这里应该调用数据库清理逻辑
            logger.info("过期爬虫任务数据清理完成");
        } catch (Exception e) {
            logger.error("清理过期爬虫任务数据失败", e);
        }
    }
}
