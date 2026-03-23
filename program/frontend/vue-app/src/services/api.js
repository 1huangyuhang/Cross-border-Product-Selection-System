/**
 * API服务层
 * 按照software.md文档要求实现前后端数据交互
 */

import axios from 'axios'

// 配置axios
const api = axios.create({
  baseURL: 'http://localhost:8080/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    console.log('发送请求:', config.method.toUpperCase(), config.url)
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('收到响应:', response.status, response.config.url)
    return response.data
  },
  error => {
    console.error('响应错误:', error.response?.status, error.message)
    return Promise.reject(error)
  }
)

/**
 * 商品相关API
 */
export const productAPI = {
  // 获取商品列表
  getProducts(params = {}) {
    return api.get('/products', { params })
  },

  // 获取商品详情
  getProductById(id) {
    return api.get(`/products/${id}`)
  },

  // 创建商品
  createProduct(data) {
    return api.post('/products', data)
  },

  // 更新商品
  updateProduct(id, data) {
    return api.put(`/products/${id}`, data)
  },

  // 删除商品
  deleteProduct(id) {
    return api.delete(`/products/${id}`)
  },

  // 获取热门商品
  getPopularProducts(limit = 10) {
    return api.get('/products/popular', { params: { limit } })
  },

  // 获取分类统计
  getCategoryStats() {
    return api.get('/products/categories/stats')
  }
}

/**
 * 爬虫相关API
 */
export const crawlerAPI = {
  // 启动爬虫
  startCrawler(params = {}) {
    return api.post('/crawler/start', null, { params })
  },

  // 停止爬虫
  stopCrawler() {
    return api.post('/crawler/stop')
  },

  // 获取爬虫状态
  getCrawlerStatus() {
    return api.get('/crawler/status')
  },

  // 获取爬虫日志
  getCrawlerLogs(params = {}) {
    return api.get('/crawler/logs', { params })
  },

  // 获取爬虫统计
  getCrawlerStats() {
    return api.get('/crawler/stats')
  }
}

/**
 * 数据分析相关API
 */
export const analysisAPI = {
  // 获取销售趋势
  getSalesTrend(days = 30) {
    return api.get('/analysis/sales/trend', { params: { days } })
  },

  // 获取商品表现
  getProductPerformance(limit = 10) {
    return api.get('/analysis/products/performance', { params: { limit } })
  },

  // 获取分类分析
  getCategoryAnalysis() {
    return api.get('/analysis/categories/analysis')
  },

  // 获取价格分析
  getPriceAnalysis(category = null) {
    return api.get('/analysis/price/analysis', { 
      params: category ? { category } : {} 
    })
  },

  // 获取市场趋势
  getMarketTrend() {
    return api.get('/analysis/market/trend')
  },

  // 获取竞品分析
  getCompetitorAnalysis(productId) {
    return api.get('/analysis/competitor/analysis', { 
      params: { productId } 
    })
  }
}

/**
 * 推荐相关API
 */
export const recommendationAPI = {
  // 获取用户推荐
  getUserRecommendations(userId, limit = 10) {
    return api.get('/recommendations/user', { 
      params: { userId, limit } 
    })
  },

  // 获取商品推荐
  getProductRecommendations(productId, limit = 10) {
    return api.get('/recommendations/product', { 
      params: { productId, limit } 
    })
  },

  // 记录用户交互
  recordInteraction(data) {
    return api.post('/recommendations/interaction', data)
  },

  // 获取推荐统计
  getRecommendationStats() {
    return api.get('/recommendations/stats')
  }
}

/**
 * 算法相关API
 */
export const algorithmAPI = {
  // 训练推荐模型
  trainModel() {
    return api.post('/algorithm/train')
  },

  // 获取模型状态
  getModelStatus() {
    return api.get('/algorithm/status')
  },

  // 生成推荐
  generateRecommendations(params) {
    return api.post('/algorithm/recommend', params)
  }
}

export default api