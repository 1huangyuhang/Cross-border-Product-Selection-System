package com.project.controller;

import com.project.service.CrawlerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 爬虫管理控制器
 * 按照software.md文档要求实现爬虫控制API
 */
@RestController
@RequestMapping("/api/crawler")
@CrossOrigin(origins = "*")
public class CrawlerController {

    @Autowired
    private CrawlerService crawlerService;

    /**
     * 启动爬虫任务
     */
    @PostMapping("/start")
    public ResponseEntity<Map<String, Object>> startCrawler(
            @RequestParam(required = false) String platform,
            @RequestParam(required = false) String category,
            @RequestParam(defaultValue = "100") int maxPages) {
        
        try {
            Map<String, Object> result = crawlerService.startCrawling(platform, category, maxPages);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 停止爬虫任务
     */
    @PostMapping("/stop")
    public ResponseEntity<Map<String, Object>> stopCrawler() {
        try {
            Map<String, Object> result = crawlerService.stopCrawling();
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 获取爬虫状态
     */
    @GetMapping("/status")
    public ResponseEntity<Map<String, Object>> getCrawlerStatus() {
        try {
            Map<String, Object> status = crawlerService.getCrawlerStatus();
            return ResponseEntity.ok(status);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 获取爬虫日志
     */
    @GetMapping("/logs")
    public ResponseEntity<Map<String, Object>> getCrawlerLogs(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size) {
        
        try {
            Map<String, Object> logs = crawlerService.getCrawlerLogs(page, size);
            return ResponseEntity.ok(logs);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 获取爬取统计
     */
    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getCrawlerStats() {
        try {
            Map<String, Object> stats = crawlerService.getCrawlerStats();
            return ResponseEntity.ok(stats);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}
