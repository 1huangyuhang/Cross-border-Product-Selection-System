<template>
  <div class="analysis">
    <h1>数据分析</h1>
    
    <div class="analysis-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['tab-button', { active: activeTab === tab.id }]"
      >
        <i :class="tab.icon"></i>
        {{ tab.name }}
      </button>
    </div>

    <div class="analysis-content">
      <!-- 销售分析 -->
      <div v-if="activeTab === 'sales'" class="tab-content">
        <h3>销售趋势分析</h3>
        <div class="chart-container">
          <div class="chart-placeholder">
            📊 销售趋势图表
            <p>显示过去30天的销售数据</p>
          </div>
        </div>
        </div>

      <!-- 商品分析 -->
      <div v-if="activeTab === 'products'" class="tab-content">
        <h3>商品表现分析</h3>
        <div class="product-stats">
          <div class="stat-item">
            <h4>热门商品</h4>
            <ul>
              <li v-for="product in topProducts" :key="product.id">
                {{ product.title }} - 销量: {{ product.sales }}
              </li>
            </ul>
          </div>
          <div class="stat-item">
            <h4>分类分布</h4>
            <div class="category-chart">
              <div v-for="category in categoryStats" :key="category.name" class="category-item">
                <span>{{ category.name }}</span>
                <div class="progress-bar">
                  <div class="progress" :style="{ width: category.percentage + '%' }"></div>
                </div>
                <span>{{ category.percentage }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 推荐分析 -->
      <div v-if="activeTab === 'recommendations'" class="tab-content">
        <h3>推荐算法分析</h3>
        <div class="recommendation-stats">
          <div class="stat-card">
            <h4>推荐准确率</h4>
            <p class="stat-number">{{ recommendationAccuracy }}%</p>
          </div>
          <div class="stat-card">
            <h4>用户点击率</h4>
            <p class="stat-number">{{ clickThroughRate }}%</p>
          </div>
          <div class="stat-card">
            <h4>转化率</h4>
            <p class="stat-number">{{ conversionRate }}%</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Analysis',
  setup() {
    const activeTab = ref('sales')
    
    const tabs = [
      { id: 'sales', name: '销售分析', icon: 'icon-chart' },
      { id: 'products', name: '商品分析', icon: 'icon-box' },
      { id: 'price', name: '价格分析', icon: 'icon-dollar' },
      { id: 'platform', name: '平台分析', icon: 'icon-globe' },
      { id: 'recommendations', name: '推荐分析', icon: 'icon-magic' }
    ]

    const topProducts = ref([
      { id: 1, title: '无线蓝牙耳机', sales: 1250 },
      { id: 2, title: '智能手表', sales: 980 },
      { id: 3, title: '便携充电宝', sales: 756 }
    ])

    const categoryStats = ref([
      { name: '电子产品', percentage: 45 },
      { name: '服装配饰', percentage: 30 },
      { name: '家居用品', percentage: 15 },
      { name: '其他', percentage: 10 }
    ])

    const recommendationAccuracy = ref(78)
    const clickThroughRate = ref(12.5)
    const conversionRate = ref(3.2)

    onMounted(() => {
      // 模拟数据加载
      console.log('数据分析页面已加载')
    })

    return {
      activeTab,
      tabs,
      topProducts,
      categoryStats,
      recommendationAccuracy,
      clickThroughRate,
      conversionRate
    }
  }
}
</script>

<style scoped>
.analysis {
  padding: 20px;
}

.analysis-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.tab-button {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tab-button.active {
  border-bottom-color: #3498db;
  color: #3498db;
}

.analysis-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart-container {
  margin: 20px 0;
}

.chart-placeholder {
  height: 300px;
  background: #f8f9fa;
  border: 2px dashed #ddd;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 1.2em;
  color: #666;
}

.product-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.stat-item h4 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.stat-item ul {
  list-style: none;
  padding: 0;
}

.stat-item li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.category-chart {
  margin-top: 15px;
}

.category-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.category-item span:first-child {
  min-width: 100px;
}

.progress-bar {
  flex: 1;
  height: 20px;
  background: #eee;
  border-radius: 10px;
  margin: 0 10px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: #3498db;
  transition: width 0.3s ease;
}

.recommendation-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.stat-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  color: #2c3e50;
  margin: 10px 0;
}
</style>
