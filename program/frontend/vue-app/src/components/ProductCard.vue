<template>
  <el-card class="product-card" :body-style="{ padding: '0px' }">
    <div class="product-image-container">
      <img :src="product.image_url || defaultImage" :alt="product.title" class="product-image" />
      <div class="product-badge" v-if="product.rating >= 4.5">
        <el-tag type="success" size="small">推荐</el-tag>
      </div>
    </div>
    
    <div class="product-info">
      <h3 class="product-title" :title="product.title">{{ product.title }}</h3>
      
      <div class="product-price">
        <span class="current-price">¥{{ formatPrice(product.price) }}</span>
        <span class="original-price" v-if="product.original_price && product.original_price > product.price">
          ¥{{ formatPrice(product.original_price) }}
        </span>
      </div>
      
      <div class="product-rating">
        <el-rate 
          v-model="product.rating" 
          disabled 
          show-score 
          text-color="#ff9900"
          score-template="{value}"
        />
        <span class="review-count">({{ product.review_count }})</span>
      </div>
      
      <div class="product-meta">
        <el-tag :type="getPlatformType(product.platform)" size="small">
          {{ product.platform }}
        </el-tag>
        <el-tag v-if="product.category" size="small">
          {{ product.category }}
        </el-tag>
      </div>
      
      <div class="product-actions">
        <el-button type="primary" size="small" @click="handleViewProduct">
          <el-icon><View /></el-icon>
          查看详情
        </el-button>
        <el-button type="success" size="small" @click="handleAddToFavorites">
          <el-icon><Star /></el-icon>
          收藏
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { View, Star } from '@element-plus/icons-vue'

// 按照software.md文档要求实现组件方法
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['view-product', 'add-to-favorites'])

// 默认图片
const defaultImage = ref('/images/default-product.png')

// 格式化价格 - 按照software.md文档要求实现数据处理方法
const formatPrice = (price) => {
  if (!price || price === 0) return '0.00'
  return Number(price).toFixed(2)
}

// 获取平台类型颜色
const getPlatformType = (platform) => {
  const platformTypes = {
    'temu': 'success',
    'aliexpress': 'warning', 
    'amazon': 'info'
  }
  return platformTypes[platform] || 'default'
}

// 处理查看商品 - 按照software.md文档要求实现事件处理
const handleViewProduct = () => {
  emit('view-product', props.product)
  ElMessage.success('正在跳转到商品详情...')
}

// 处理添加到收藏 - 按照software.md文档要求实现事件处理
const handleAddToFavorites = () => {
  emit('add-to-favorites', props.product)
  ElMessage.success('已添加到收藏夹')
}

// 组件挂载时的处理 - 按照software.md文档要求实现mounted方法
import { onMounted } from 'vue'

onMounted(() => {
  console.log('ProductCard component mounted for product:', props.product.id)
})
</script>

<style scoped>
.product-card {
  margin-bottom: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-image-container {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.product-badge {
  position: absolute;
  top: 8px;
  right: 8px;
}

.product-info {
  padding: 16px;
}

.product-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
  line-height: 1.4;
  height: 2.8em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #333;
}

.product-price {
  margin-bottom: 12px;
}

.current-price {
  font-size: 20px;
  font-weight: bold;
  color: #e74c3c;
  margin-right: 8px;
}

.original-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
}

.product-rating {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.review-count {
  margin-left: 8px;
  font-size: 12px;
  color: #666;
}

.product-meta {
  margin-bottom: 16px;
}

.product-meta .el-tag {
  margin-right: 8px;
  margin-bottom: 4px;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.product-actions .el-button {
  flex: 1;
}
</style>
