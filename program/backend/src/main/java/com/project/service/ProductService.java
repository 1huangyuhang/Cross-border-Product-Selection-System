package com.project.service;

import com.project.entity.Product;
import com.project.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * 商品服务层
 * 按照software.md文档要求实现业务逻辑
 */
@Service
public class ProductService {

    @Autowired
    private ProductRepository productRepository;

    /**
     * 获取商品列表 - 支持分页、分类筛选、关键词搜索
     */
    public Page<Product> getProducts(Pageable pageable, String category, String keyword) {
        if (category != null && !category.isEmpty()) {
            if (keyword != null && !keyword.isEmpty()) {
                return productRepository.findByCategoryAndTitleContainingIgnoreCase(category, keyword, pageable);
            } else {
                return productRepository.findByCategory(category, pageable);
            }
        } else if (keyword != null && !keyword.isEmpty()) {
            return productRepository.findByTitleContainingIgnoreCase(keyword, pageable);
        } else {
            return productRepository.findAll(pageable);
        }
    }

    /**
     * 根据ID获取商品
     */
    public Product getProductById(Long id) {
        Optional<Product> product = productRepository.findById(id);
        if (product.isPresent()) {
            return product.get();
        } else {
            throw new RuntimeException("商品不存在");
        }
    }

    /**
     * 保存商品
     */
    public Product saveProduct(Product product) {
        return productRepository.save(product);
    }

    /**
     * 删除商品
     */
    public void deleteProduct(Long id) {
        productRepository.deleteById(id);
    }

    /**
     * 获取热门商品
     */
    public List<Product> getPopularProducts(int limit) {
        return productRepository.findTopSellingProducts(org.springframework.data.domain.PageRequest.of(0, limit));
    }

    /**
     * 获取分类统计
     */
    public List<Map<String, Object>> getCategoryStats() {
        List<Object[]> results = productRepository.getCategoryStats();
        return results.stream()
                .map(row -> Map.of(
                    "category", row[0],
                    "count", row[1],
                    "avgPrice", row[2],
                    "avgRating", row[3]
                ))
                .toList();
    }
}