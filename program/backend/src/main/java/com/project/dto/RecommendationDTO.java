package com.project.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

/**
 * 推荐结果数据传输对象
 * 按照software.md文档要求实现推荐系统DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RecommendationDTO {
    
    private Long userId;
    private List<RecommendedProduct> recommendedProducts;
    private String algorithmType;
    private LocalDateTime generatedAt;
    
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class RecommendedProduct {
        private Long productId;
        private String title;
        private BigDecimal price;
        private BigDecimal rating;
        private String imageUrl;
        private String category;
        private String brand;
        private BigDecimal score;
        private Integer rankPosition;
        private String reason; // 推荐理由
    }
}
