<template>
  <div class="recommend">
    <div class="recommend-header">
      <h1>智能推荐系统</h1>
      <div class="header-actions">
        <button @click="refreshRecommendations" class="btn btn-outline" :disabled="loading">
          <i class="icon-refresh" :class="{ 'spinning': loading }"></i>
          刷新推荐
        </button>
        <button @click="exportRecommendations" class="btn btn-success">
          <i class="icon-download"></i>
          导出推荐
        </button>
      </div>
    </div>
    
    <!-- 推荐算法选择 -->
    <div class="algorithm-selector">
      <h3>推荐算法</h3>
      <div class="algorithm-tabs">
        <button 
          v-for="algorithm in algorithms" 
          :key="algorithm.id"
          @click="selectedAlgorithm = algorithm.id"
          :class="['algorithm-btn', { active: selectedAlgorithm === algorithm.id }]"
        >
          <i :class="algorithm.icon"></i>
          {{ algorithm.name }}
          <span class="algorithm-desc">{{ algorithm.description }}</span>
        </button>
      </div>
    </div>
    
    <!-- 推荐控制面板 -->
    <div class="recommend-controls">
      <div class="control-section">
        <h3>推荐设置</h3>
        <div class="control-grid">
          <div class="control-item">
            <label>推荐数量:</label>
            <input v-model.number="recommendCount" type="number" min="5" max="50" class="control-input">
          </div>
          <div class="control-item">
            <label>用户ID:</label>
            <input v-model="userId" placeholder="输入用户ID" class="control-input">
          </div>
          <div class="control-item">
            <label>商品分类:</label>
            <select v-model="selectedCategory" class="control-select">
              <option value="">所有分类</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>
          <div class="control-item">
            <label>价格范围:</label>
            <div class="price-range">
              <input v-model.number="minPrice" type="number" placeholder="最低价" class="price-input">
              <span>-</span>
              <input v-model.number="maxPrice" type="number" placeholder="最高价" class="price-input">
            </div>
          </div>
        </div>
      </div>
      
      <div class="action-section">
        <button @click="generateRecommendations" 
                :disabled="loading || !userId" 
                class="btn btn-primary btn-large">
          <i class="icon-magic"></i>
          {{ loading ? '生成中...' : '生成推荐' }}
        </button>
        <button @click="clearRecommendations" class="btn btn-warning">
          <i class="icon-trash"></i>
          清空推荐
        </button>
      </div>
    </div>

    <!-- 推荐结果 -->
    <div class="recommendations-section">
      <div class="section-header">
        <h3>推荐结果</h3>
        <div class="result-info">
          <span v-if="recommendations.length > 0">
            共 {{ recommendations.length }} 个推荐商品
          </span>
          <span v-if="selectedAlgorithm" class="algorithm-info">
            使用算法: {{ getAlgorithmName(selectedAlgorithm) }}
          </span>
        </div>
      </div>
      
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>正在生成推荐...</p>
      </div>
      
      <div v-else-if="recommendations.length === 0" class="empty-state">
        <i class="icon-magic"></i>
        <h3>暂无推荐</h3>
        <p>请设置推荐参数并点击"生成推荐"按钮</p>
      </div>
      
      <div v-else class="recommendations-grid">
        <div v-for="(recommendation, index) in recommendations" 
             :key="recommendation.id" 
             class="recommendation-card"
             :class="{ 'top-recommendation': index < 3 }">
          
          <div class="card-header">
            <div class="recommendation-rank">
              <span class="rank-number">{{ index + 1 }}</span>
              <span class="rank-badge" v-if="index < 3">推荐</span>
            </div>
            <div class="recommendation-score">
              <div class="score-circle" :class="getScoreClass(recommendation.score)">
                {{ recommendation.score.toFixed(1) }}
              </div>
              <span class="score-label">推荐分数</span>
            </div>
          </div>
          
          <div class="product-image-container">
            <img :src="recommendation.product.imageUrl || '/placeholder-product.jpg'" 
                 :alt="recommendation.product.title" 
                 class="product-image"
                 @error="handleImageError">
            <div class="product-badges">
              <span v-if="recommendation.product.isAvailable" class="badge available">有货</span>
              <span v-if="recommendation.product.rating >= 4.5" class="badge high-rating">高评分</span>
            </div>
          </div>
          
          <div class="product-info">
            <h4 class="product-title" :title="recommendation.product.title">
              {{ recommendation.product.title }}
            </h4>
            
            <div class="product-meta">
              <span class="platform">{{ recommendation.product.platform }}</span>
              <span class="category">{{ recommendation.product.category }}</span>
            </div>
            
            <div class="product-price">
              <span class="current-price">¥{{ formatPrice(recommendation.product.price) }}</span>
              <span v-if="recommendation.product.originalPrice && recommendation.product.originalPrice > recommendation.product.price" 
                    class="original-price">¥{{ formatPrice(recommendation.product.originalPrice) }}</span>
            </div>
            
            <div class="product-stats">
              <div class="rating">
                <i class="icon-star"></i>
                <span>{{ recommendation.product.rating || 0 }}</span>
                <span class="review-count">({{ recommendation.product.reviewCount || 0 }})</span>
              </div>
              <div class="sales">
                <i class="icon-shopping"></i>
                <span>销量: {{ formatNumber(recommendation.product.salesCount || 0) }}</span>
              </div>
            </div>
            
            <div class="recommendation-reason">
              <h5>推荐理由:</h5>
              <p>{{ recommendation.reason }}</p>
            </div>
            
            <div class="product-actions">
              <button @click="viewProduct(recommendation.product)" class="btn btn-sm btn-primary">
                <i class="icon-eye"></i>
                查看详情
              </button>
              <button @click="addToFavorites(recommendation.product)" class="btn btn-sm btn-outline">
                <i class="icon-heart"></i>
                收藏
              </button>
              <button @click="feedbackRecommendation(recommendation, 'like')" class="btn btn-sm btn-success">
                <i class="icon-thumbs-up"></i>
                喜欢
              </button>
              <button @click="feedbackRecommendation(recommendation, 'dislike')" class="btn btn-sm btn-danger">
                <i class="icon-thumbs-down"></i>
                不喜欢
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 推荐统计 -->
    <div v-if="recommendations.length > 0" class="recommendation-stats">
      <h3>推荐统计</h3>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">🎯</div>
          <div class="stat-content">
            <h4>平均推荐分数</h4>
            <p class="stat-value">{{ averageScore.toFixed(1) }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-content">
            <h4>平均价格</h4>
            <p class="stat-value">¥{{ formatNumber(averagePrice) }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-content">
            <h4>平均评分</h4>
            <p class="stat-value">{{ averageRating.toFixed(1) }}/5</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📊</div>
          <div class="stat-content">
            <h4>算法准确率</h4>
            <p class="stat-value">{{ algorithmAccuracy }}%</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Recommend',
  setup() {
    const recommendations = ref([])

    const generateRecommendations = () => {
      // 模拟生成推荐
      recommendations.value = [
        {
          id: 1,
          product: {
            title: '智能手表',
            price: 299.99,
            imageUrl: 'https://via.placeholder.com/200x200'
          },
          score: 9.2,
          reason: '基于您的浏览历史，这款智能手表与您的兴趣高度匹配'
        },
        {
          id: 2,
          product: {
            title: '无线充电器',
            price: 89.99,
            imageUrl: 'https://via.placeholder.com/200x200'
          },
          score: 8.7,
          reason: '与您购买的其他电子产品完美搭配'
        }
      ]
    }

    const refreshRecommendations = () => {
      generateRecommendations()
    }

    onMounted(() => {
      generateRecommendations()
    })

    return {
      recommendations,
      generateRecommendations,
      refreshRecommendations
    }
  }
}
</script>

<style scoped>
.recommend {
  padding: 20px;
}

.recommend-controls {
  margin-bottom: 30px;
}

.btn {
  padding: 10px 20px;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.recommendation-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  gap: 15px;
}

.product-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
}

.product-info {
  flex: 1;
}

.product-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.1em;
}

.price {
  font-size: 1.2em;
  font-weight: bold;
  color: #e74c3c;
  margin: 5px 0;
}

.score {
  color: #27ae60;
  font-weight: bold;
  margin: 5px 0;
}

.reason {
  font-size: 0.9em;
  color: #666;
  margin: 5px 0;
}
</style>
