package com.project.repository;

import com.project.entity.Product;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * 商品数据访问层
 */
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    
    /**
     * 根据平台和平台ID查找商品
     */
    Optional<Product> findByPlatformAndPlatformId(String platform, String platformId);
    
    /**
     * 根据关键词搜索商品标题
     */
    @Query("SELECT p FROM Product p WHERE p.title LIKE %:keyword% OR p.keywords LIKE %:keyword%")
    List<Product> findByKeyword(@Param("keyword") String keyword);
    
    /**
     * 根据分类查找商品
     */
    List<Product> findByCategory(String category);
    
    /**
     * 根据品牌查找商品
     */
    List<Product> findByBrand(String brand);
    
    /**
     * 根据价格范围查找商品
     */
    List<Product> findByPriceBetween(BigDecimal minPrice, BigDecimal maxPrice);
    
    /**
     * 根据评分范围查找商品
     */
    List<Product> findByRatingBetween(BigDecimal minRating, BigDecimal maxRating);
    
    /**
     * 根据销量范围查找商品
     */
    List<Product> findBySalesCountBetween(Integer minSales, Integer maxSales);
    
    /**
     * 查找可用商品
     */
    List<Product> findByIsAvailableTrue();
    
    /**
     * 根据平台查找商品
     */
    List<Product> findByPlatform(String platform);
    
    /**
     * 根据爬取时间范围查找商品
     */
    List<Product> findByCrawlDateBetween(LocalDateTime startDate, LocalDateTime endDate);
    
    /**
     * 分页查询商品
     */
    Page<Product> findAll(Pageable pageable);
    
    /**
     * 根据分类分页查询
     */
    Page<Product> findByCategory(String category, Pageable pageable);
    
    /**
     * 根据品牌分页查询
     */
    Page<Product> findByBrand(String brand, Pageable pageable);
    
    /**
     * 复杂查询：根据多个条件查找商品
     */
    @Query("SELECT p FROM Product p WHERE " +
           "(:category IS NULL OR p.category = :category) AND " +
           "(:brand IS NULL OR p.brand = :brand) AND " +
           "(:minPrice IS NULL OR p.price >= :minPrice) AND " +
           "(:maxPrice IS NULL OR p.price <= :maxPrice) AND " +
           "(:minRating IS NULL OR p.rating >= :minRating) AND " +
           "(:minSales IS NULL OR p.salesCount >= :minSales)")
    Page<Product> findProductsByConditions(
            @Param("category") String category,
            @Param("brand") String brand,
            @Param("minPrice") BigDecimal minPrice,
            @Param("maxPrice") BigDecimal maxPrice,
            @Param("minRating") BigDecimal minRating,
            @Param("minSales") Integer minSales,
            Pageable pageable);
    
    /**
     * 统计商品数量
     */
    @Query("SELECT COUNT(p) FROM Product p WHERE p.isAvailable = true")
    Long countAvailableProducts();
    
    /**
     * 统计各分类商品数量
     */
    @Query("SELECT p.category, COUNT(p) FROM Product p GROUP BY p.category")
    List<Object[]> countProductsByCategory();
    
    /**
     * 统计各品牌商品数量
     */
    @Query("SELECT p.brand, COUNT(p) FROM Product p GROUP BY p.brand")
    List<Object[]> countProductsByBrand();
    
    /**
     * 获取平均价格
     */
    @Query("SELECT AVG(p.price) FROM Product p WHERE p.price IS NOT NULL")
    BigDecimal getAveragePrice();
    
    /**
     * 获取平均评分
     */
    @Query("SELECT AVG(p.rating) FROM Product p WHERE p.rating IS NOT NULL")
    BigDecimal getAverageRating();
    
    /**
     * 获取平均销量
     */
    @Query("SELECT AVG(p.salesCount) FROM Product p WHERE p.salesCount IS NOT NULL")
    BigDecimal getAverageSales();
    
    /**
     * 获取热门商品（按销量排序）
     */
    @Query("SELECT p FROM Product p WHERE p.isAvailable = true ORDER BY p.salesCount DESC")
    List<Product> findTopSellingProducts(Pageable pageable);
    
    /**
     * 获取高评分商品
     */
    @Query("SELECT p FROM Product p WHERE p.rating >= :minRating AND p.isAvailable = true ORDER BY p.rating DESC")
    List<Product> findHighRatedProducts(@Param("minRating") BigDecimal minRating, Pageable pageable);
    
    /**
     * 根据分类和品牌查找商品（用于推荐系统）
     */
    List<Product> findByCategoryAndBrand(String category, String brand);
    
    /**
     * 获取分类统计信息
     */
    @Query("SELECT p.category, COUNT(p), AVG(p.price), AVG(p.rating) FROM Product p GROUP BY p.category")
    List<Object[]> getCategoryStats();
    
    
    /**
     * 根据标题模糊查询
     */
    Page<Product> findByTitleContainingIgnoreCase(String title, Pageable pageable);
    
    /**
     * 根据分类和标题模糊查询
     */
    Page<Product> findByCategoryAndTitleContainingIgnoreCase(String category, String title, Pageable pageable);
}
