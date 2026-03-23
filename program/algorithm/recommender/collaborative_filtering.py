#!/usr/bin/env python3
"""
协同过滤推荐算法
基于用户行为数据进行商品推荐
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import logging

logger = logging.getLogger(__name__)

class CollaborativeFiltering:
    """协同过滤推荐算法"""
    
    def __init__(self, n_factors=50, n_epochs=20, lr=0.01, reg=0.01):
        """
        初始化协同过滤模型
        
        Args:
            n_factors: 潜在因子数量
            n_epochs: 训练轮数
            lr: 学习率
            reg: 正则化参数
        """
        self.n_factors = n_factors
        self.n_epochs = n_epochs
        self.lr = lr
        self.reg = reg
        self.user_factors = None
        self.item_factors = None
        self.user_biases = None
        self.item_biases = None
        self.global_bias = None
        self.is_fitted = False
        
    def fit(self, user_item_matrix):
        """
        训练协同过滤模型
        
        Args:
            user_item_matrix: 用户-物品评分矩阵 (用户ID, 物品ID, 评分)
        """
        logger.info("开始训练协同过滤模型...")
        
        # 转换为用户-物品矩阵
        pivot_matrix = user_item_matrix.pivot_table(
            index='user_id', 
            columns='item_id', 
            values='rating', 
            fill_value=0
        )
        
        # 获取用户和物品数量
        n_users, n_items = pivot_matrix.shape
        self.n_users = n_users
        self.n_items = n_items
        
        # 初始化参数
        self.user_factors = np.random.normal(0, 0.1, (n_users, self.n_factors))
        self.item_factors = np.random.normal(0, 0.1, (n_items, self.n_factors))
        self.user_biases = np.zeros(n_users)
        self.item_biases = np.zeros(n_items)
        self.global_bias = pivot_matrix.values[pivot_matrix.values > 0].mean()
        
        # 训练模型
        for epoch in range(self.n_epochs):
            total_error = 0
            count = 0
            
            for user_idx in range(n_users):
                for item_idx in range(n_items):
                    if pivot_matrix.iloc[user_idx, item_idx] > 0:
                        # 计算预测评分
                        pred = (self.global_bias + 
                               self.user_biases[user_idx] + 
                               self.item_biases[item_idx] + 
                               np.dot(self.user_factors[user_idx], self.item_factors[item_idx]))
                        
                        # 计算误差
                        actual = pivot_matrix.iloc[user_idx, item_idx]
                        error = actual - pred
                        total_error += error ** 2
                        count += 1
                        
                        # 更新参数
                        self.user_biases[user_idx] += self.lr * (error - self.reg * self.user_biases[user_idx])
                        self.item_biases[item_idx] += self.lr * (error - self.reg * self.item_biases[item_idx])
                        
                        # 更新因子
                        user_factor_grad = error * self.item_factors[item_idx] - self.reg * self.user_factors[user_idx]
                        item_factor_grad = error * self.user_factors[user_idx] - self.reg * self.item_factors[item_idx]
                        
                        self.user_factors[user_idx] += self.lr * user_factor_grad
                        self.item_factors[item_idx] += self.lr * item_factor_grad
            
            rmse = np.sqrt(total_error / count) if count > 0 else 0
            logger.info(f"Epoch {epoch + 1}/{self.n_epochs}, RMSE: {rmse:.4f}")
        
        self.is_fitted = True
        logger.info("协同过滤模型训练完成")
    
    def predict(self, user_id, item_id):
        """
        预测用户对物品的评分
        
        Args:
            user_id: 用户ID
            item_id: 物品ID
            
        Returns:
            预测评分
        """
        if not self.is_fitted:
            raise ValueError("模型尚未训练，请先调用fit方法")
        
        # 获取用户和物品的索引
        user_idx = self._get_user_index(user_id)
        item_idx = self._get_item_index(item_id)
        
        if user_idx is None or item_idx is None:
            return self.global_bias
        
        # 计算预测评分
        pred = (self.global_bias + 
               self.user_biases[user_idx] + 
               self.item_biases[item_idx] + 
               np.dot(self.user_factors[user_idx], self.item_factors[item_idx]))
        
        return max(1.0, min(5.0, pred))  # 限制评分范围在1-5之间
    
    def recommend_items(self, user_id, n_recommendations=10):
        """
        为用户推荐物品
        
        Args:
            user_id: 用户ID
            n_recommendations: 推荐数量
            
        Returns:
            推荐物品列表
        """
        if not self.is_fitted:
            raise ValueError("模型尚未训练，请先调用fit方法")
        
        user_idx = self._get_user_index(user_id)
        if user_idx is None:
            return []
        
        # 计算用户对所有物品的预测评分
        predictions = []
        for item_idx in range(self.n_items):
            pred = (self.global_bias + 
                   self.user_biases[user_idx] + 
                   self.item_biases[item_idx] + 
                   np.dot(self.user_factors[user_idx], self.item_factors[item_idx]))
            predictions.append((item_idx, pred))
        
        # 按评分排序，返回前N个推荐
        predictions.sort(key=lambda x: x[1], reverse=True)
        return [item_idx for item_idx, _ in predictions[:n_recommendations]]
    
    def _get_user_index(self, user_id):
        """获取用户索引"""
        # 这里需要根据实际的用户ID映射到矩阵索引
        # 简化实现，实际应用中需要维护ID到索引的映射
        return user_id - 1 if 1 <= user_id <= self.n_users else None
    
    def _get_item_index(self, item_id):
        """获取物品索引"""
        # 这里需要根据实际的物品ID映射到矩阵索引
        # 简化实现，实际应用中需要维护ID到索引的映射
        return item_id - 1 if 1 <= item_id <= self.n_items else None
    
    def get_similar_users(self, user_id, n_similar=10):
        """
        获取相似用户
        
        Args:
            user_id: 用户ID
            n_similar: 相似用户数量
            
        Returns:
            相似用户列表
        """
        if not self.is_fitted:
            raise ValueError("模型尚未训练，请先调用fit方法")
        
        user_idx = self._get_user_index(user_id)
        if user_idx is None:
            return []
        
        # 计算用户相似度
        similarities = []
        for other_user_idx in range(self.n_users):
            if other_user_idx != user_idx:
                sim = cosine_similarity(
                    self.user_factors[user_idx].reshape(1, -1),
                    self.user_factors[other_user_idx].reshape(1, -1)
                )[0][0]
                similarities.append((other_user_idx, sim))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [user_idx for user_idx, _ in similarities[:n_similar]]
    
    def get_similar_items(self, item_id, n_similar=10):
        """
        获取相似物品
        
        Args:
            item_id: 物品ID
            n_similar: 相似物品数量
            
        Returns:
            相似物品列表
        """
        if not self.is_fitted:
            raise ValueError("模型尚未训练，请先调用fit方法")
        
        item_idx = self._get_item_index(item_id)
        if item_idx is None:
            return []
        
        # 计算物品相似度
        similarities = []
        for other_item_idx in range(self.n_items):
            if other_item_idx != item_idx:
                sim = cosine_similarity(
                    self.item_factors[item_idx].reshape(1, -1),
                    self.item_factors[other_item_idx].reshape(1, -1)
                )[0][0]
                similarities.append((other_item_idx, sim))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [item_idx for item_idx, _ in similarities[:n_similar]]
