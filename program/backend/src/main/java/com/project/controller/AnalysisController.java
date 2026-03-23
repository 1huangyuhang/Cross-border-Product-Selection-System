package com.project.controller;

import com.project.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 数据分析控制器
 * 按照software.md文档要求实现数据分析API
 */
@RestController
@RequestMapping("/api/analysis")
@CrossOrigin(origins = "*")
public class AnalysisController {

    @Autowired
    private ProductRepository productRepository;

    /**
     * 获取销售趋势分析
     */
    @GetMapping("/sales/trend")
    public ResponseEntity<Map<String, Object>> getSalesTrend(
            @RequestParam(defaultValue = "30") int days) {
        
        try {
            // 简化实现：返回基本统计信息
            Map<String, Object> trend = new HashMap<>();
            trend.put("totalProducts", productRepository.count());
            trend.put("days", days);
            trend.put("message", "销售趋势分析功能");
            return ResponseEntity.ok(trend);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 获取商品表现分析
     */
    @GetMapping("/products/performance")
    public ResponseEntity<Map<String, Object>> getProductPerformance(
            @RequestParam(defaultValue = "10") int limit) {
        
        try {
            // 简化实现：返回基本统计信息
            Map<String, Object> performance = new HashMap<>();
            performance.put("totalProducts", productRepository.count());
            performance.put("limit", limit);
            performance.put("message", "商品表现分析功能");
            return ResponseEntity.ok(performance);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 获取分类分析
     */
    @GetMapping("/categories/analysis")
    public ResponseEntity<Map<String, Object>> getCategoryAnalysis() {
        try {
            // 简化实现：返回基本统计信息
            Map<String, Object> analysis = new HashMap<>();
            analysis.put("totalProducts", productRepository.count());
            analysis.put("message", "分类分析功能");
            return ResponseEntity.ok(analysis);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 获取价格分析
     */
    @GetMapping("/price/analysis")
    public ResponseEntity<Map<String, Object>> getPriceAnalysis() {
        try {
            // 简化实现：返回基本统计信息
            Map<String, Object> analysis = new HashMap<>();
            analysis.put("totalProducts", productRepository.count());
            analysis.put("message", "价格分析功能");
            return ResponseEntity.ok(analysis);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    /**
     * 获取市场分析
     */
    @GetMapping("/market/analysis")
    public ResponseEntity<Map<String, Object>> getMarketAnalysis() {
        try {
            // 简化实现：返回基本统计信息
            Map<String, Object> analysis = new HashMap<>();
            analysis.put("totalProducts", productRepository.count());
            analysis.put("message", "市场分析功能");
            return ResponseEntity.ok(analysis);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}