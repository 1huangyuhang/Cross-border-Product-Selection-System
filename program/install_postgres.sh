#!/bin/bash

# 安装PostgreSQL数据库（macOS）
echo "🗄️ 安装PostgreSQL数据库..."

# 检查是否已安装PostgreSQL
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL已安装"
    psql --version
else
    echo "📦 安装PostgreSQL..."
    
    # 使用Homebrew安装PostgreSQL
    if command -v brew &> /dev/null; then
        echo "使用Homebrew安装PostgreSQL..."
        brew install postgresql@15
        
        # 启动PostgreSQL服务
        echo "🔄 启动PostgreSQL服务..."
        brew services start postgresql@15
        
        # 等待服务启动
        sleep 5
        
        # 创建数据库和用户
        echo "🗄️ 创建数据库和用户..."
        createdb ecommerce_db
        psql -d ecommerce_db -c "CREATE USER postgres WITH PASSWORD 'password';"
        psql -d ecommerce_db -c "GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO postgres;"
        
        echo "✅ PostgreSQL安装完成"
        echo "   数据库: ecommerce_db"
        echo "   用户: postgres"
        echo "   密码: password"
        echo "   端口: 5432"
        
    else
        echo "❌ 请先安装Homebrew"
        echo "💡 安装Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
fi

echo "✅ PostgreSQL数据库准备完成！"
