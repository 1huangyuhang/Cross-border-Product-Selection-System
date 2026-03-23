/**
 * 跨境电商选品系统 - 主应用JavaScript文件
 * 管理所有前端逻辑和交互
 */

// Vue应用配置
const { createApp, ref, onMounted } = Vue;
const { ElMessage, ElMessageBox } = ElementPlus;

// 创建Vue应用
const app = createApp({
    setup() {
        // 响应式数据
        const loading = ref(false);
        const sidebarCollapsed = ref(false);
        const currentPage = ref('dashboard');
        const notifications = ref(3);
        
        // 统计数据
        const stats = ref({
            totalProducts: 1250,
            totalSales: 15680,
            avgPrice: 25.99,
            avgRating: 4.2
        });
        
        // 数据管理相关
        const tables = ref([]);
        const loadingTables = ref(false);
        
        // 爬虫管理相关
        const crawlerRunning = ref(false);
        const crawlerStatus = ref(null);
        
        // 数据分析相关
        const analysisLoading = ref(false);
        const sampleLoading = ref(false);
        const analysisResult = ref(null);
        
        // API配置
        const API_BASE_URL = 'http://localhost:5000/api';
        
        // 方法定义
        const toggleSidebar = () => {
            sidebarCollapsed.value = !sidebarCollapsed.value;
        };
        
        const navigateTo = (page) => {
            currentPage.value = page;
        };
        
        const getPageTitle = () => {
            const titles = {
                dashboard: '仪表盘',
                data: '数据管理',
                crawler: '爬虫管理',
                analysis: '数据分析',
                products: '商品管理',
                settings: '系统设置'
            };
            return titles[currentPage.value] || '未知页面';
        };
        
        // 数据管理方法
        const refreshTables = async () => {
            try {
                loadingTables.value = true;
                const response = await fetch(`${API_BASE_URL}/temu-tables`);
                const data = await response.json();
                
                if (data.success) {
                    tables.value = data.tables || [];
                    ElMessage.success(`成功获取 ${tables.value.length} 个表`);
                } else {
                    throw new Error(data.message || '获取表列表失败');
                }
            } catch (error) {
                console.error('获取表列表出错：', error);
                ElMessage.error('获取表列表失败：' + error.message);
            } finally {
                loadingTables.value = false;
            }
        };
        
        const viewTableData = (tableName) => {
            ElMessage.info(`查看表 ${tableName} 的数据`);
            // 这里可以打开模态框或跳转到详细页面
        };
        
        // 爬虫管理方法
        const startCrawler = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/crawler/start`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    crawlerRunning.value = true;
                    crawlerStatus.value = data.data;
                    ElMessage.success('爬虫启动成功');
                } else {
                    throw new Error(data.message || '启动爬虫失败');
                }
            } catch (error) {
                console.error('启动爬虫出错：', error);
                ElMessage.error('启动爬虫失败：' + error.message);
            }
        };
        
        const pauseCrawler = () => {
            ElMessage.info('爬虫已暂停');
        };
        
        const stopCrawler = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/crawler/stop`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    crawlerRunning.value = false;
                    crawlerStatus.value = null;
                    ElMessage.success('爬虫已停止');
                } else {
                    throw new Error(data.message || '停止爬虫失败');
                }
            } catch (error) {
                console.error('停止爬虫出错：', error);
                ElMessage.error('停止爬虫失败：' + error.message);
            }
        };
        
        // 数据分析方法
        const startAnalysis = async () => {
            try {
                analysisLoading.value = true;
                analysisResult.value = null;
                
                // 模拟分析过程
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // 模拟分析结果
                analysisResult.value = {
                    basic_stats: {
                        total_products: 150,
                        avg_price: 25.99,
                        avg_rating: 4.2,
                        avg_sales: 1250
                    },
                    price_analysis: {
                        mean_price: 25.99,
                        price_range: [5.99, 99.99]
                    },
                    sales_analysis: {
                        avg_sales: 1250,
                        total_sales: 187500
                    },
                    rating_analysis: {
                        avg_rating: 4.2,
                        rating_distribution: {
                            '5星': 45,
                            '4星': 35,
                            '3星': 15,
                            '2星': 3,
                            '1星': 2
                        }
                    },
                    chart_data: {
                        price_distribution: {
                            labels: ['$0-10', '$10-20', '$20-30', '$30+'],
                            data: [25, 40, 30, 5]
                        },
                        sales_distribution: {
                            labels: ['0-500', '500-1000', '1000-2000', '2000+'],
                            data: [30, 35, 25, 10]
                        },
                        rating_distribution: {
                            labels: ['1-2星', '3星', '4星', '5星'],
                            data: [5, 15, 35, 45]
                        },
                        keyword_cloud: [
                            { text: '手机', weight: 10 },
                            { text: '配件', weight: 8 },
                            { text: '保护套', weight: 6 },
                            { text: '充电器', weight: 5 },
                            { text: '耳机', weight: 4 }
                        ]
                    },
                    predictions: {
                        market_opportunity: 'high',
                        price_competitiveness: 'high',
                        quality_indicators: 'good',
                        recommendations: [
                            '建议关注价格竞争力',
                            '考虑优化产品描述',
                            '关注用户评价反馈'
                        ]
                    }
                };
                
                ElMessage.success('数据分析完成');
                
                // 延迟渲染图表，确保DOM已更新
                setTimeout(() => {
                    renderCharts();
                }, 100);
                
            } catch (error) {
                console.error('数据分析出错：', error);
                ElMessage.error('数据分析失败：' + error.message);
            } finally {
                analysisLoading.value = false;
            }
        };
        
        const loadSampleData = async () => {
            try {
                sampleLoading.value = true;
                
                const response = await fetch(`${API_BASE_URL}/analysis/sample-data`);
                const data = await response.json();
                
                if (data.success) {
                    ElMessage.success('示例数据加载完成');
                } else {
                    throw new Error(data.message || '加载示例数据失败');
                }
            } catch (error) {
                console.error('加载示例数据出错：', error);
                ElMessage.error('加载示例数据失败：' + error.message);
            } finally {
                sampleLoading.value = false;
            }
        };
        
        // 图表渲染方法
        const renderCharts = () => {
            if (!analysisResult.value || !analysisResult.value.chart_data) {
                return;
            }
            
            const chartData = analysisResult.value.chart_data;
            
            // 渲染价格分布图表
            const priceChartElement = document.querySelector('canvas[ref="priceChart"]');
            if (priceChartElement && chartData.price_distribution) {
                const ctx = priceChartElement.getContext('2d');
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: chartData.price_distribution.labels,
                        datasets: [{
                            data: chartData.price_distribution.data,
                            backgroundColor: [
                                '#FF6384',
                                '#36A2EB',
                                '#FFCE56',
                                '#4BC0C0'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
            }
            
            // 渲染销量分布图表
            const salesChartElement = document.querySelector('canvas[ref="salesChart"]');
            if (salesChartElement && chartData.sales_distribution) {
                const ctx = salesChartElement.getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: chartData.sales_distribution.labels,
                        datasets: [{
                            label: '商品数量',
                            data: chartData.sales_distribution.data,
                            backgroundColor: '#36A2EB'
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
            
            // 渲染评分分布图表
            const ratingChartElement = document.querySelector('canvas[ref="ratingChart"]');
            if (ratingChartElement && chartData.rating_distribution) {
                const ctx = ratingChartElement.getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: chartData.rating_distribution.labels,
                        datasets: [{
                            data: chartData.rating_distribution.data,
                            backgroundColor: [
                                '#FF6384',
                                '#FF9F40',
                                '#4BC0C0',
                                '#9966FF'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }
                });
            }
        };
        
        // 获取市场机会类型
        const getOpportunityType = (opportunity) => {
            switch (opportunity) {
                case 'high': return 'success';
                case 'medium': return 'warning';
                case 'low': return 'danger';
                default: return 'info';
            }
        };
        
        const getOpportunityText = (opportunity) => {
            switch (opportunity) {
                case 'high': return '高机会';
                case 'medium': return '中等机会';
                case 'low': return '低机会';
                default: return '未知';
            }
        };
        
        // 获取竞争力类型
        const getCompetitivenessType = (competitiveness) => {
            switch (competitiveness) {
                case 'high': return 'success';
                case 'medium': return 'warning';
                case 'low': return 'danger';
                default: return 'info';
            }
        };
        
        const getCompetitivenessText = (competitiveness) => {
            switch (competitiveness) {
                case 'high': return '高竞争力';
                case 'medium': return '中等竞争力';
                case 'low': return '低竞争力';
                default: return '未知';
            }
        };
        
        // 获取质量类型
        const getQualityType = (quality) => {
            switch (quality) {
                case 'high': return 'success';
                case 'medium': return 'warning';
                case 'low': return 'danger';
                default: return 'info';
            }
        };
        
        const getQualityText = (quality) => {
            switch (quality) {
                case 'high': return '高质量';
                case 'medium': return '中等质量';
                case 'low': return '低质量';
                default: return '未知';
            }
        };
        
        // 组件挂载时初始化
        onMounted(() => {
            // 初始化数据
            refreshTables();
            
            // 检查系统健康状态
            checkSystemHealth();
        });
        
        // 检查系统健康状态
        const checkSystemHealth = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/health`);
                const data = await response.json();
                
                if (data.status === 'healthy') {
                    console.log('系统健康检查通过');
                } else {
                    ElMessage.warning('系统健康检查异常');
                }
            } catch (error) {
                console.error('系统健康检查失败：', error);
                ElMessage.error('无法连接到后端服务');
            }
        };
        
        // 返回组件公开的属性和方法
        return {
            loading,
            sidebarCollapsed,
            currentPage,
            notifications,
            stats,
            tables,
            loadingTables,
            crawlerRunning,
            crawlerStatus,
            analysisLoading,
            sampleLoading,
            analysisResult,
            toggleSidebar,
            navigateTo,
            getPageTitle,
            refreshTables,
            viewTableData,
            startCrawler,
            pauseCrawler,
            stopCrawler,
            startAnalysis,
            loadSampleData,
            renderCharts,
            getOpportunityType,
            getOpportunityText,
            getCompetitivenessType,
            getCompetitivenessText,
            getQualityType,
            getQualityText
        };
    }
});

// 注册Element Plus组件
app.use(ElementPlus);

// 挂载应用
app.mount('#app');
