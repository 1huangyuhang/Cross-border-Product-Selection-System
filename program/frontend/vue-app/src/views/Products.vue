<template>
  <div class="products">
    <div class="products-header">
      <h1>商品管理</h1>
      <div class="header-actions">
        <button @click="refreshProducts" class="btn btn-outline" :disabled="loading">
          <i class="icon-refresh" :class="{ 'spinning': loading }"></i>
          刷新
        </button>
        <button @click="exportProducts" class="btn btn-success">
          <i class="icon-download"></i>
          导出
        </button>
      </div>
    </div>
    
    <!-- 筛选和搜索 -->
    <div class="filters-section">
      <div class="filters">
        <div class="search-box">
          <i class="icon-search"></i>
          <input 
            v-model="searchQuery" 
            placeholder="搜索商品标题、品牌、关键词..." 
            class="search-input"
            @input="handleSearch"
          >
        </div>
        
        <select v-model="selectedCategory" @change="handleCategoryChange" class="category-select">
          <option value="">所有分类</option>
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
        
        <select v-model="selectedPlatform" @change="handlePlatformChange" class="platform-select">
          <option value="">所有平台</option>
          <option value="temu">Temu</option>
          <option value="aliexpress">AliExpress</option>
          <option value="amazon">Amazon</option>
        </select>
        
        <select v-model="sortBy" @change="handleSortChange" class="sort-select">
          <option value="createdAt">最新上架</option>
          <option value="price">价格排序</option>
          <option value="rating">评分排序</option>
          <option value="salesCount">销量排序</option>
        </select>
      </div>
      
      <!-- 统计信息 -->
      <div class="stats-info">
        <span class="total-count">共 {{ totalProducts }} 个商品</span>
        <span class="filtered-count" v-if="filteredProducts.length !== totalProducts">
          筛选后: {{ filteredProducts.length }} 个
        </span>
      </div>
    </div>
    
    <!-- 商品列表 -->
    <div class="products-container">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>加载商品中...</p>
      </div>
      
      <div v-else-if="filteredProducts.length === 0" class="empty-state">
        <i class="icon-box"></i>
        <h3>暂无商品</h3>
        <p>没有找到符合条件的商品，请尝试调整筛选条件</p>
      </div>
      
      <div v-else class="products-grid">
        <div v-for="product in paginatedProducts" :key="product.id" class="product-card">
          <div class="product-image-container">
            <img 
              :src="product.imageUrl || '/placeholder-product.jpg'" 
              :alt="product.title" 
              class="product-image"
              @error="handleImageError"
            >
            <div class="product-badges">
              <span v-if="product.isAvailable" class="badge available">有货</span>
              <span v-else class="badge unavailable">缺货</span>
              <span v-if="product.rating >= 4.5" class="badge high-rating">高评分</span>
            </div>
          </div>
          
          <div class="product-info">
            <h3 class="product-title" :title="product.title">{{ product.title }}</h3>
            
            <div class="product-meta">
              <span class="platform">{{ product.platform }}</span>
              <span class="category">{{ product.category }}</span>
            </div>
            
            <div class="product-price">
              <span class="current-price">¥{{ formatPrice(product.price) }}</span>
              <span v-if="product.originalPrice && product.originalPrice > product.price" 
                    class="original-price">¥{{ formatPrice(product.originalPrice) }}</span>
            </div>
            
            <div class="product-stats">
              <div class="rating">
                <i class="icon-star"></i>
                <span>{{ product.rating || 0 }}</span>
                <span class="review-count">({{ product.reviewCount || 0 }})</span>
              </div>
              <div class="sales">
                <i class="icon-shopping"></i>
                <span>销量: {{ formatNumber(product.salesCount || 0) }}</span>
              </div>
            </div>
            
            <div class="product-actions">
              <button @click="viewProduct(product)" class="btn btn-sm btn-outline">
                <i class="icon-eye"></i>
                查看
              </button>
              <button @click="addToFavorites(product)" class="btn btn-sm btn-outline">
                <i class="icon-heart"></i>
                收藏
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 分页 -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        @click="goToPage(currentPage - 1)" 
        :disabled="currentPage <= 0"
        class="btn btn-outline"
      >
        上一页
      </button>
      
      <div class="page-numbers">
        <button 
          v-for="page in visiblePages" 
          :key="page"
          @click="goToPage(page - 1)"
          :class="{ 'active': page - 1 === currentPage }"
          class="page-btn"
        >
          {{ page }}
        </button>
      </div>
      
      <button 
        @click="goToPage(currentPage + 1)" 
        :disabled="currentPage >= totalPages - 1"
        class="btn btn-outline"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Products',
  setup() {
    const store = useStore()
    
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const currentPage = ref(0)
    const pageSize = ref(10)
    const loading = ref(false)

    // 从store获取数据
    const products = computed(() => store.getters.products)
    const productLoading = computed(() => store.getters.productLoading)
    const productError = computed(() => store.getters.productError)

    const filteredProducts = computed(() => {
      let filtered = products.value
      
      if (searchQuery.value) {
        filtered = filtered.filter(p => 
          p.title.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
      }
      
      if (selectedCategory.value) {
        filtered = filtered.filter(p => p.category === selectedCategory.value)
      }
      
      return filtered
    })

    onMounted(async () => {
      await loadProducts()
    })

    // 监听搜索条件变化
    watch([searchQuery, selectedCategory], async () => {
      await loadProducts()
    })

    const loadProducts = async () => {
      try {
        loading.value = true
        
        const params = {
          page: currentPage.value,
          size: pageSize.value
        }
        
        if (searchQuery.value) {
          params.keyword = searchQuery.value
        }
        
        if (selectedCategory.value) {
          params.category = selectedCategory.value
        }
        
        await store.dispatch('fetchProducts', params)
        
      } catch (error) {
        console.error('加载商品失败:', error)
      } finally {
        loading.value = false
      }
    }

    const handleSearch = async () => {
      currentPage.value = 0
      await loadProducts()
    }

    const handleCategoryChange = async () => {
      currentPage.value = 0
      await loadProducts()
    }

    const loadMore = async () => {
      currentPage.value++
      await loadProducts()
    }

    return {
      products,
      searchQuery,
      selectedCategory,
      filteredProducts,
      loading,
      productLoading,
      productError,
      handleSearch,
      handleCategoryChange,
      loadMore
    }
  }
}
</script>

<style scoped>
.products {
  padding: 20px;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search-input, .category-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.product-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.price {
  font-size: 1.2em;
  font-weight: bold;
  color: #e74c3c;
  margin: 10px 0;
}
</style>
