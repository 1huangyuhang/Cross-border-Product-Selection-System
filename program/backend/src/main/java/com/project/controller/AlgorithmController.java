package com.project.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;
import java.util.List;

/**
 * 算法服务控制器
 * 根据software.md文档要求实现后端调用算法模块
 */
@RestController
@RequestMapping("/api/algorithm")
@CrossOrigin(origins = "*")
public class AlgorithmController {
    
    private static final Logger logger = LoggerFactory.getLogger(AlgorithmController.class);
    
    @Autowired
    private RestTemplate restTemplate;
    
    private static final String ALGORITHM_SERVICE_URL = "http://localhost:8082";
    
    /**
     * 获取商品推荐
     * 调用算法模块的协同过滤推荐
     */
    @PostMapping("/recommend")
    public ResponseEntity<Map<String, Object>> getRecommendations(@RequestBody Map<String, Object> request) {
        try {
            logger.info("开始获取商品推荐: {}", request);
            
            // 调用算法服务获取推荐
            String recommendUrl = ALGORITHM_SERVICE_URL + "/recommend";
            
            // 构建推荐请求
            Map<String, Object> recommendRequest = new HashMap<>();
            recommendRequest.put("userId", request.get("userId"));
            recommendRequest.put("limit", request.getOrDefault("limit", 10));
            recommendRequest.put("algorithm", "collaborative_filtering");
            
            // 调用算法服务
            Map<String, Object> response = restTemplate.postForObject(
                recommendUrl, recommendRequest, Map.class);
            
            logger.info("商品推荐获取成功");
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            logger.error("获取商品推荐失败", e);
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "推荐服务暂时不可用");
            errorResponse.put("message", e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 开始数据分析
     * 调用算法模块进行数据分析
     */
    @PostMapping("/analyze")
    public ResponseEntity<Map<String, Object>> startAnalysis(@RequestBody Map<String, Object> request) {
        try {
            logger.info("开始数据分析: {}", request);
            
            // 调用算法服务进行数据分析
            String analyzeUrl = ALGORITHM_SERVICE_URL + "/analyze";
            
            // 构建分析请求
            Map<String, Object> analyzeRequest = new HashMap<>();
            analyzeRequest.put("dataType", request.get("dataType"));
            analyzeRequest.put("timeRange", request.get("timeRange"));
            analyzeRequest.put("analysisType", request.get("analysisType"));
            
            // 调用算法服务
            Map<String, Object> response = restTemplate.postForObject(
                analyzeUrl, analyzeRequest, Map.class);
            
            logger.info("数据分析完成");
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            logger.error("数据分析失败", e);
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "分析服务暂时不可用");
            errorResponse.put("message", e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 获取相似商品
     * 基于内容推荐算法
     */
    @GetMapping("/similar/{productId}")
    public ResponseEntity<Map<String, Object>> getSimilarProducts(@PathVariable Long productId) {
        try {
            logger.info("获取相似商品: {}", productId);
            
            // 调用算法服务获取相似商品
            String similarUrl = ALGORITHM_SERVICE_URL + "/similar/" + productId;
            
            Map<String, Object> response = restTemplate.getForObject(similarUrl, Map.class);
            
            logger.info("相似商品获取成功");
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            logger.error("获取相似商品失败", e);
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "相似商品服务暂时不可用");
            errorResponse.put("message", e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 训练推荐模型
     * 调用算法模块训练新的推荐模型
     */
    @PostMapping("/train")
    public ResponseEntity<Map<String, Object>> trainModel(@RequestBody Map<String, Object> request) {
        try {
            logger.info("开始训练推荐模型: {}", request);
            
            // 调用算法服务训练模型
            String trainUrl = ALGORITHM_SERVICE_URL + "/train";
            
            // 构建训练请求
            Map<String, Object> trainRequest = new HashMap<>();
            trainRequest.put("modelType", request.get("modelType"));
            trainRequest.put("dataSize", request.get("dataSize"));
            trainRequest.put("parameters", request.get("parameters"));
            
            // 调用算法服务
            Map<String, Object> response = restTemplate.postForObject(
                trainUrl, trainRequest, Map.class);
            
            logger.info("推荐模型训练完成");
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            logger.error("训练推荐模型失败", e);
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "模型训练服务暂时不可用");
            errorResponse.put("message", e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 获取算法服务状态
     */
    @GetMapping("/status")
    public ResponseEntity<Map<String, Object>> getAlgorithmStatus() {
        try {
            logger.info("检查算法服务状态");
            
            // 调用算法服务健康检查
            String healthUrl = ALGORITHM_SERVICE_URL + "/health";
            
            Map<String, Object> response = restTemplate.getForObject(healthUrl, Map.class);
            
            logger.info("算法服务状态检查完成");
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            logger.error("检查算法服务状态失败", e);
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("status", "DOWN");
            errorResponse.put("error", "算法服务不可用");
            errorResponse.put("message", e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
    
    /**
     * 获取推荐算法列表
     */
    @GetMapping("/algorithms")
    public ResponseEntity<Map<String, Object>> getAvailableAlgorithms() {
        try {
            logger.info("获取可用推荐算法列表");
            
            // 返回可用的推荐算法
            Map<String, Object> algorithms = new HashMap<>();
            algorithms.put("collaborative_filtering", "协同过滤推荐");
            algorithms.put("content_based", "基于内容的推荐");
            algorithms.put("hybrid", "混合推荐算法");
            algorithms.put("deep_learning", "深度学习推荐");
            
            Map<String, Object> response = new HashMap<>();
            response.put("algorithms", algorithms);
            response.put("status", "success");
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            logger.error("获取推荐算法列表失败", e);
            Map<String, Object> errorResponse = new HashMap<>();
            errorResponse.put("error", "获取算法列表失败");
            errorResponse.put("message", e.getMessage());
            return ResponseEntity.status(500).body(errorResponse);
        }
    }
}
