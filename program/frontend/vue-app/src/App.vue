<template>
  <div id="app">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="260px" class="sidebar">
        <div class="logo">
          <i class="el-icon-data-analysis"></i>
          <span>选品系统</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="dashboard">
            <i class="el-icon-s-home"></i>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="products">
            <i class="el-icon-goods"></i>
            <span>商品管理</span>
          </el-menu-item>
          <el-menu-item index="crawler">
            <i class="el-icon-download"></i>
            <span>爬虫管理</span>
          </el-menu-item>
          <el-menu-item index="analysis">
            <i class="el-icon-data-line"></i>
            <span>数据分析</span>
          </el-menu-item>
          <el-menu-item index="recommend">
            <i class="el-icon-star-on"></i>
            <span>推荐系统</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header class="header">
          <div class="header-left">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item>{{ currentPageTitle }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <el-button type="text" @click="refreshData">
              <i class="el-icon-refresh"></i>
              刷新
            </el-button>
          </div>
        </el-header>

        <!-- 内容区域 -->
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const store = useStore()
    
    const activeMenu = ref('dashboard')
    
    const currentPageTitle = computed(() => {
      const titles = {
        dashboard: '仪表盘',
        products: '商品管理',
        crawler: '爬虫管理',
        analysis: '数据分析',
        recommend: '推荐系统'
      }
      return titles[route.name] || '未知页面'
    })
    
    const handleMenuSelect = (index) => {
      activeMenu.value = index
      router.push({ name: index })
    }
    
    const refreshData = () => {
      store.dispatch('refreshAllData')
    }
    
    return {
      activeMenu,
      currentPageTitle,
      handleMenuSelect,
      refreshData
    }
  }
}
</script>

<style scoped>
.sidebar {
  background: #304156;
  color: white;
}

.logo {
  padding: 20px;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #434a50;
}

.sidebar-menu {
  border: none;
  background: #304156;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.main-content {
  background: #f5f5f5;
  padding: 20px;
}
</style>
