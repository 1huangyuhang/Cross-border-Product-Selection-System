/**
 * Vuex状态管理
 * 按照software.md文档要求实现状态管理
 */

import { createStore } from 'vuex'
import { productAPI, crawlerAPI, analysisAPI, recommendationAPI } from '../services/api'

const store = createStore({
  state: {
    // 商品相关状态
    products: [],
    currentProduct: null,
    productLoading: false,
    productError: null,
    
    // 爬虫相关状态
    crawlerStatus: {
      isRunning: false,
      crawledCount: 0,
      successCount: 0,
      successRate: 0
    },
    crawlerLogs: [],
    crawlerLoading: false,
    
    // 分析相关状态
    salesTrend: [],
    productPerformance: [],
    categoryAnalysis: {},
    priceAnalysis: {},
    marketTrend: {},
    
    // 推荐相关状态
    recommendations: [],
    recommendationStats: {},
    
    // 用户状态
    user: null,
    userInteractions: []
  },

  mutations: {
    // 商品相关mutations
    SET_PRODUCTS(state, products) {
      state.products = products
    },
    
    SET_CURRENT_PRODUCT(state, product) {
      state.currentProduct = product
    },
    
    SET_PRODUCT_LOADING(state, loading) {
      state.productLoading = loading
    },
    
    SET_PRODUCT_ERROR(state, error) {
      state.productError = error
    },
    
    // 爬虫相关mutations
    SET_CRAWLER_STATUS(state, status) {
      state.crawlerStatus = status
    },
    
    SET_CRAWLER_LOGS(state, logs) {
      state.crawlerLogs = logs
    },
    
    SET_CRAWLER_LOADING(state, loading) {
      state.crawlerLoading = loading
    },
    
    // 分析相关mutations
    SET_SALES_TREND(state, trend) {
      state.salesTrend = trend
    },
    
    SET_PRODUCT_PERFORMANCE(state, performance) {
      state.productPerformance = performance
    },
    
    SET_CATEGORY_ANALYSIS(state, analysis) {
      state.categoryAnalysis = analysis
    },
    
    SET_PRICE_ANALYSIS(state, analysis) {
      state.priceAnalysis = analysis
    },
    
    SET_MARKET_TREND(state, trend) {
      state.marketTrend = trend
    },
    
    // 推荐相关mutations
    SET_RECOMMENDATIONS(state, recommendations) {
      state.recommendations = recommendations
    },
    
    SET_RECOMMENDATION_STATS(state, stats) {
      state.recommendationStats = stats
    },
    
    // 用户相关mutations
    SET_USER(state, user) {
      state.user = user
    },
    
    SET_USER_INTERACTIONS(state, interactions) {
      state.userInteractions = interactions
    }
  },

  actions: {
    // 商品相关actions
    async fetchProducts({ commit }, params = {}) {
      try {
        commit('SET_PRODUCT_LOADING', true)
        commit('SET_PRODUCT_ERROR', null)
        
        const response = await productAPI.getProducts(params)
        commit('SET_PRODUCTS', response.products || [])
        
        return response
      } catch (error) {
        commit('SET_PRODUCT_ERROR', error.message)
        throw error
      } finally {
        commit('SET_PRODUCT_LOADING', false)
      }
    },

    async fetchProductById({ commit }, id) {
      try {
        commit('SET_PRODUCT_LOADING', true)
        const product = await productAPI.getProductById(id)
        commit('SET_CURRENT_PRODUCT', product)
        return product
      } catch (error) {
        commit('SET_PRODUCT_ERROR', error.message)
        throw error
      } finally {
        commit('SET_PRODUCT_LOADING', false)
      }
    },

    async createProduct({ dispatch }, productData) {
      try {
        await productAPI.createProduct(productData)
        // 重新获取商品列表
        await dispatch('fetchProducts')
      } catch (error) {
        throw error
      }
    },

    async updateProduct({ dispatch }, { id, data }) {
      try {
        await productAPI.updateProduct(id, data)
        // 重新获取商品列表
        await dispatch('fetchProducts')
      } catch (error) {
        throw error
      }
    },

    async deleteProduct({ dispatch }, id) {
      try {
        await productAPI.deleteProduct(id)
        // 重新获取商品列表
        await dispatch('fetchProducts')
      } catch (error) {
        throw error
      }
    },

    async fetchPopularProducts({ commit }) {
      try {
        const response = await productAPI.getPopularProducts()
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchCategoryStats({ commit }) {
      try {
        const response = await productAPI.getCategoryStats()
        return response
      } catch (error) {
        throw error
      }
    },

    // 爬虫相关actions
    async startCrawler({ commit, dispatch }, params = {}) {
      try {
        commit('SET_CRAWLER_LOADING', true)
        const response = await crawlerAPI.startCrawler(params)
        
        // 启动后获取状态
        await dispatch('fetchCrawlerStatus')
        return response
      } catch (error) {
        throw error
      } finally {
        commit('SET_CRAWLER_LOADING', false)
      }
    },

    async stopCrawler({ commit, dispatch }) {
      try {
        const response = await crawlerAPI.stopCrawler()
        
        // 停止后获取状态
        await dispatch('fetchCrawlerStatus')
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchCrawlerStatus({ commit }) {
      try {
        const status = await crawlerAPI.getCrawlerStatus()
        commit('SET_CRAWLER_STATUS', status)
        return status
      } catch (error) {
        throw error
      }
    },

    async fetchCrawlerLogs({ commit }, params = {}) {
      try {
        const response = await crawlerAPI.getCrawlerLogs(params)
        commit('SET_CRAWLER_LOGS', response.logs || [])
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchCrawlerStats({ commit }) {
      try {
        const stats = await crawlerAPI.getCrawlerStats()
        return stats
      } catch (error) {
        throw error
      }
    },

    // 分析相关actions
    async fetchSalesTrend({ commit }, days = 30) {
      try {
        const response = await analysisAPI.getSalesTrend(days)
        commit('SET_SALES_TREND', response.trendData || [])
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchProductPerformance({ commit }, limit = 10) {
      try {
        const response = await analysisAPI.getProductPerformance(limit)
        commit('SET_PRODUCT_PERFORMANCE', response.topProducts || [])
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchCategoryAnalysis({ commit }) {
      try {
        const response = await analysisAPI.getCategoryAnalysis()
        commit('SET_CATEGORY_ANALYSIS', response)
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchPriceAnalysis({ commit }, category = null) {
      try {
        const response = await analysisAPI.getPriceAnalysis(category)
        commit('SET_PRICE_ANALYSIS', response)
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchMarketTrend({ commit }) {
      try {
        const response = await analysisAPI.getMarketTrend()
        commit('SET_MARKET_TREND', response)
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchCompetitorAnalysis({ commit }, productId) {
      try {
        const response = await analysisAPI.getCompetitorAnalysis(productId)
        return response
      } catch (error) {
        throw error
      }
    },

    // 推荐相关actions
    async fetchUserRecommendations({ commit }, { userId, limit = 10 }) {
      try {
        const response = await recommendationAPI.getUserRecommendations(userId, limit)
        commit('SET_RECOMMENDATIONS', response)
        return response
      } catch (error) {
        throw error
      }
    },

    async fetchProductRecommendations({ commit }, { productId, limit = 10 }) {
      try {
        const response = await recommendationAPI.getProductRecommendations(productId, limit)
        return response
      } catch (error) {
        throw error
      }
    },

    async recordUserInteraction({ commit }, interactionData) {
      try {
        await recommendationAPI.recordInteraction(interactionData)
        // 可以在这里更新本地状态
      } catch (error) {
        throw error
      }
    },

    async fetchRecommendationStats({ commit }) {
      try {
        const stats = await recommendationAPI.getRecommendationStats()
        commit('SET_RECOMMENDATION_STATS', stats)
        return stats
      } catch (error) {
        throw error
      }
    }
  },

  getters: {
    // 商品相关getters
    products: state => state.products,
    currentProduct: state => state.currentProduct,
    productLoading: state => state.productLoading,
    productError: state => state.productError,
    
    // 爬虫相关getters
    crawlerStatus: state => state.crawlerStatus,
    crawlerLogs: state => state.crawlerLogs,
    crawlerLoading: state => state.crawlerLoading,
    
    // 分析相关getters
    salesTrend: state => state.salesTrend,
    productPerformance: state => state.productPerformance,
    categoryAnalysis: state => state.categoryAnalysis,
    priceAnalysis: state => state.priceAnalysis,
    marketTrend: state => state.marketTrend,
    
    // 推荐相关getters
    recommendations: state => state.recommendations,
    recommendationStats: state => state.recommendationStats,
    
    // 用户相关getters
    user: state => state.user,
    userInteractions: state => state.userInteractions
  }
})

export default store