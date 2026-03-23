package com.project.repository;

import com.project.entity.UserInteraction;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserInteractionRepository extends JpaRepository<UserInteraction, Long> {
    
    List<UserInteraction> findByUserId(Long userId);
    
    List<UserInteraction> findByProductId(Long productId);
    
    List<UserInteraction> findByUserIdAndInteractionType(Long userId, String interactionType);
    
    @Query("SELECT ui FROM UserInteraction ui WHERE ui.userId = :userId ORDER BY ui.createdDate DESC")
    List<UserInteraction> findByUserIdOrderByCreatedDateDesc(@Param("userId") Long userId);
    
    @Query("SELECT COUNT(ui) FROM UserInteraction ui WHERE ui.productId = :productId")
    Long countByProductId(@Param("productId") Long productId);
    
    @Query("SELECT AVG(ui.rating) FROM UserInteraction ui WHERE ui.productId = :productId AND ui.rating IS NOT NULL")
    Double getAverageRatingByProductId(@Param("productId") Long productId);
}
