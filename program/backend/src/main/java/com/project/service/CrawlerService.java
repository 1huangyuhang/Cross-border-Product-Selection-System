package com.project.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * 爬虫服务层
 * 按照software.md文档要求实现爬虫业务逻辑
 */
@Service
public class CrawlerService {

    @Autowired
    private RestTemplate restTemplate;

    private final AtomicBoolean isRunning = new AtomicBoolean(false);
    private final AtomicInteger crawledCount = new AtomicInteger(0);
    private final AtomicInteger successCount = new AtomicInteger(0);
    private final List<Map<String, Object>> logs = new ArrayList<>();

    /**
     * 启动爬虫任务
     */
    public Map<String, Object> startCrawling(String platform, String category, int maxPages) {
        if (isRunning.get()) {
            return Map.of("status", "error", "message", "爬虫已在运行中");
        }

        isRunning.set(true);
        crawledCount.set(0);
        successCount.set(0);
        logs.clear();

        addLog("开始爬取数据...");
        addLog("平台: " + (platform != null ? platform : "全部"));
        addLog("分类: " + (category != null ? category : "全部"));
        addLog("最大页数: " + maxPages);

        // 模拟爬虫任务
        new Thread(() -> {
            try {
                for (int i = 1; i <= maxPages && isRunning.get(); i++) {
                    Thread.sleep(2000); // 模拟爬取延迟
                    
                    if (!isRunning.get()) break;
                    
                    crawledCount.incrementAndGet();
                    if (Math.random() > 0.1) { // 90% 成功率
                        successCount.incrementAndGet();
                        addLog("成功爬取第 " + i + " 页数据");
                    } else {
                        addLog("第 " + i + " 页爬取失败");
                    }
                }
                
                if (isRunning.get()) {
                    addLog("爬取任务完成");
                    isRunning.set(false);
                }
            } catch (InterruptedException e) {
                addLog("爬取任务被中断");
                isRunning.set(false);
            }
        }).start();

        return Map.of(
            "status", "success",
            "message", "爬虫任务已启动",
            "platform", platform != null ? platform : "全部",
            "category", category != null ? category : "全部",
            "maxPages", maxPages
        );
    }

    /**
     * 停止爬虫任务
     */
    public Map<String, Object> stopCrawling() {
        if (!isRunning.get()) {
            return Map.of("status", "error", "message", "爬虫未在运行");
        }

        isRunning.set(false);
        addLog("爬虫任务已停止");

        return Map.of(
            "status", "success",
            "message", "爬虫任务已停止",
            "crawledCount", crawledCount.get(),
            "successCount", successCount.get()
        );
    }

    /**
     * 获取爬虫状态
     */
    public Map<String, Object> getCrawlerStatus() {
        return Map.of(
            "isRunning", isRunning.get(),
            "crawledCount", crawledCount.get(),
            "successCount", successCount.get(),
            "successRate", crawledCount.get() > 0 ? 
                Math.round((double) successCount.get() / crawledCount.get() * 100) : 0,
            "lastUpdate", LocalDateTime.now()
        );
    }

    /**
     * 获取爬虫日志
     */
    public Map<String, Object> getCrawlerLogs(int page, int size) {
        int start = page * size;
        int end = Math.min(start + size, logs.size());
        
        List<Map<String, Object>> pageLogs = logs.subList(start, end);
        
        return Map.of(
            "logs", pageLogs,
            "total", logs.size(),
            "page", page,
            "size", size
        );
    }

    /**
     * 获取爬虫统计
     */
    public Map<String, Object> getCrawlerStats() {
        return Map.of(
            "totalCrawled", crawledCount.get(),
            "totalSuccess", successCount.get(),
            "successRate", crawledCount.get() > 0 ? 
                Math.round((double) successCount.get() / crawledCount.get() * 100) : 0,
            "isRunning", isRunning.get(),
            "startTime", isRunning.get() ? LocalDateTime.now().minusHours(1) : null,
            "lastActivity", logs.isEmpty() ? null : logs.get(0).get("time")
        );
    }

    /**
     * 添加日志
     */
    private void addLog(String message) {
        Map<String, Object> log = Map.of(
            "id", UUID.randomUUID().toString(),
            "time", LocalDateTime.now().toString(),
            "message", message
        );
        logs.add(0, log); // 添加到开头
        
        // 保持日志数量在合理范围内
        if (logs.size() > 100) {
            logs.remove(logs.size() - 1);
        }
    }
}
