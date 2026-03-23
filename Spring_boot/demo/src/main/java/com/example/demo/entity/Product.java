package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 商品实体类
 * 对应数据库中的products表
 */
@Entity
@Table(name = "products")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Product {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "title", nullable = false, length = 500)
    private String title;
    
    @Column(name = "price", precision = 10, scale = 2)
    private BigDecimal price;
    
    @Column(name = "original_price", precision = 10, scale = 2)
    private BigDecimal originalPrice;
    
    @Column(name = "rating", precision = 3, scale = 2)
    private BigDecimal rating;
    
    @Column(name = "review_count")
    private Integer reviewCount;
    
    @Column(name = "sales_count")
    private Integer salesCount;
    
    @Column(name = "image_url", length = 1000)
    private String imageUrl;
    
    @Column(name = "product_url", length = 1000)
    private String productUrl;
    
    @Column(name = "category", length = 100)
    private String category;
    
    @Column(name = "brand", length = 100)
    private String brand;
    
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "keywords", length = 500)
    private String keywords;
    
    @Column(name = "platform", length = 50)
    private String platform;
    
    @Column(name = "platform_id", length = 100)
    private String platformId;
    
    @Column(name = "is_available")
    private Boolean isAvailable;
    
    @Column(name = "crawl_date")
    private LocalDateTime crawlDate;
    
    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    // 构造函数
    public Product(String title, BigDecimal price, BigDecimal rating, Integer salesCount) {
        this.title = title;
        this.price = price;
        this.rating = rating;
        this.salesCount = salesCount;
        this.isAvailable = true;
        this.crawlDate = LocalDateTime.now();
    }
}
