<template>
  <div class="crawler">
    <div class="crawler-header">
      <h1>爬虫管理</h1>
      <div class="header-actions">
        <button @click="refreshStatus" class="btn btn-outline" :disabled="loading">
          <i class="icon-refresh" :class="{ 'spinning': loading }"></i>
          刷新状态
        </button>
        <button @click="clearLogs" class="btn btn-warning">
          <i class="icon-trash"></i>
          清空日志
        </button>
      </div>
    </div>
    
    <!-- 爬虫控制面板 -->
    <div class="crawler-controls">
      <div class="control-section">
        <h3>爬虫控制</h3>
        <div class="control-buttons">
          <button 
            @click="startCrawling" 
            :disabled="isCrawling || loading" 
            class="btn btn-primary btn-large"
          >
            <i class="icon-play"></i>
            {{ isCrawling ? '爬取中...' : '开始爬取' }}
          </button>
          <button 
            @click="stopCrawling" 
            :disabled="!isCrawling || loading" 
            class="btn btn-danger btn-large"
          >
            <i class="icon-stop"></i>
            停止爬取
          </button>
          <button 
            @click="pauseCrawling" 
            :disabled="!isCrawling || isPaused" 
            class="btn btn-warning btn-large"
          >
            <i class="icon-pause"></i>
            {{ isPaused ? '已暂停' : '暂停爬取' }}
          </button>
        </div>
      </div>
      
      <!-- 爬虫配置 -->
      <div class="config-section">
        <h3>爬虫配置</h3>
        <div class="config-grid">
          <div class="config-item">
            <label>目标平台:</label>
            <select v-model="selectedPlatform" class="config-select">
              <option value="all">所有平台</option>
              <option value="temu">Temu</option>
              <option value="aliexpress">AliExpress</option>
              <option value="amazon">Amazon</option>
            </select>
          </div>
          <div class="config-item">
            <label>关键词:</label>
            <input v-model="searchKeywords" placeholder="输入搜索关键词" class="config-input">
          </div>
          <div class="config-item">
            <label>最大页数:</label>
            <input v-model.number="maxPages" type="number" min="1" max="100" class="config-input">
          </div>
          <div class="config-item">
            <label>延迟时间(秒):</label>
            <input v-model.number="delaySeconds" type="number" min="1" max="10" class="config-input">
          </div>
        </div>
      </div>
    </div>

    <!-- 爬虫状态 -->
    <div class="crawler-status">
      <h3>爬虫状态</h3>
      <div class="status-grid">
        <div class="status-card" :class="statusClass">
          <div class="status-icon">
            <i class="icon-status"></i>
          </div>
          <div class="status-content">
            <h4>运行状态</h4>
            <p class="status-text">{{ statusText }}</p>
          </div>
        </div>
        
        <div class="status-card">
          <div class="status-icon">
            <i class="icon-products"></i>
          </div>
          <div class="status-content">
            <h4>已爬取商品</h4>
            <p class="status-number">{{ formatNumber(crawledCount) }}</p>
          </div>
        </div>
        
        <div class="status-card">
          <div class="status-icon">
            <i class="icon-success"></i>
          </div>
          <div class="status-content">
            <h4>成功率</h4>
            <p class="status-number">{{ successRate }}%</p>
          </div>
        </div>
        
        <div class="status-card">
          <div class="status-icon">
            <i class="icon-time"></i>
          </div>
          <div class="status-content">
            <h4>运行时间</h4>
            <p class="status-text">{{ runningTime }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 实时进度 -->
    <div v-if="isCrawling" class="progress-section">
      <h3>爬取进度</h3>
      <div class="progress-container">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <div class="progress-text">
          {{ currentPage }} / {{ maxPages }} 页 ({{ progressPercentage }}%)
        </div>
      </div>
    </div>

    <!-- 爬虫日志 -->
    <div class="crawler-logs">
      <div class="logs-header">
        <h3>爬取日志</h3>
        <div class="logs-controls">
          <select v-model="logLevel" class="log-filter">
            <option value="all">所有级别</option>
            <option value="info">信息</option>
            <option value="warning">警告</option>
            <option value="error">错误</option>
          </select>
          <button @click="toggleAutoScroll" class="btn btn-sm" :class="{ 'active': autoScroll }">
            <i class="icon-scroll"></i>
            自动滚动
          </button>
        </div>
      </div>
      
      <div class="logs-container" ref="logsContainer">
        <div v-for="log in filteredLogs" :key="log.id" 
             :class="['log-item', log.level]"
             v-show="logLevel === 'all' || log.level === logLevel">
          <span class="log-time">{{ formatTime(log.time) }}</span>
          <span class="log-level">{{ log.level.toUpperCase() }}</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
        
        <div v-if="logs.length === 0" class="empty-logs">
          <i class="icon-document"></i>
          <p>暂无日志记录</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Crawler',
  setup() {
    const store = useStore()
    
    const platform = ref('temu')
    const category = ref('')
    const maxPages = ref(10)
    const loading = ref(false)

    // 从store获取数据
    const crawlerStatus = computed(() => store.getters.crawlerStatus)
    const crawlerLogs = computed(() => store.getters.crawlerLogs)
    const crawlerLoading = computed(() => store.getters.crawlerLoading)

    const statusText = computed(() => {
      return crawlerStatus.value.isRunning ? '运行中' : '已停止'
    })

    const statusClass = computed(() => {
      return crawlerStatus.value.isRunning ? 'status-running' : 'status-stopped'
    })

    const successRate = computed(() => {
      return crawlerStatus.value.successRate || 0
    })

    onMounted(async () => {
      await loadCrawlerData()
    })

    const loadCrawlerData = async () => {
      try {
        await store.dispatch('fetchCrawlerStatus')
        await store.dispatch('fetchCrawlerLogs')
      } catch (error) {
        console.error('加载爬虫数据失败:', error)
      }
    }

    const startCrawling = async () => {
      try {
        loading.value = true
        
        const params = {
          platform: platform.value,
          category: category.value,
          maxPages: maxPages.value
        }
        
        await store.dispatch('startCrawler', params)
        
        // 启动后刷新状态和日志
        await loadCrawlerData()
        
      } catch (error) {
        console.error('启动爬虫失败:', error)
      } finally {
        loading.value = false
      }
    }

    const stopCrawling = async () => {
      try {
        loading.value = true
        
        await store.dispatch('stopCrawler')
        
        // 停止后刷新状态
        await loadCrawlerData()
        
      } catch (error) {
        console.error('停止爬虫失败:', error)
      } finally {
        loading.value = false
      }
    }

    const refreshStatus = async () => {
      await loadCrawlerData()
    }

    return {
      platform,
      category,
      maxPages,
      loading,
      crawlerStatus,
      crawlerLogs,
      crawlerLoading,
      statusText,
      statusClass,
      successRate,
      startCrawling,
      stopCrawling,
      refreshStatus
    }
  }
}
</script>

<style scoped>
.crawler {
  padding: 20px;
}

.crawler-controls {
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

.btn-danger {
  background: #e74c3c;
  color: white;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.crawler-status {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.status-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.status-running {
  color: #27ae60;
  font-weight: bold;
}

.status-stopped {
  color: #e74c3c;
  font-weight: bold;
}

.crawler-logs {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.logs-container {
  max-height: 300px;
  overflow-y: auto;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
}

.log-item {
  display: flex;
  margin-bottom: 5px;
  font-family: monospace;
  font-size: 0.9em;
}

.log-time {
  color: #666;
  margin-right: 10px;
  min-width: 80px;
}
</style>
