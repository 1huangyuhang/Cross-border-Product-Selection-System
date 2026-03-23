# Spring Boot 应用

## 项目说明
这是一个完整的Spring Boot应用，用于TEMU跨境电商选品数据分析系统。

## 项目结构
```
demo/
├── src/
│   ├── main/
│   │   ├── java/com/example/demo/
│   │   │   ├── DemoApplication.java          # 主启动类
│   │   │   └── controller/
│   │   │       └── HelloController.java     # 测试控制器
│   │   └── resources/
│   │       └── application.properties       # 配置文件
│   └── test/
├── pom.xml                                  # Maven配置文件
└── start.sh                                 # 启动脚本
```

## 运行方式

### 方式1：使用Maven命令
```bash
cd Spring_boot/demo
mvn spring-boot:run
```

### 方式2：使用启动脚本
```bash
cd Spring_boot/demo
chmod +x start.sh
./start.sh
```

### 方式3：编译后运行
```bash
cd Spring_boot/demo
mvn clean compile
mvn spring-boot:run
```

## 测试接口

应用启动后，可以访问以下接口：

- `http://localhost:8081/` - 首页
- `http://localhost:8081/hello` - Hello接口
- `http://localhost:8081/health` - 健康检查
- `http://localhost:8081/actuator/health` - 系统健康检查

## 功能特性

- ✅ Spring Boot 3.4.10
- ✅ Java 17
- ✅ Web Starter
- ✅ 自动配置
- ✅ 内嵌Tomcat服务器
- ✅ RESTful API

## 故障排除

如果遇到问题：

1. 确保Java 17已安装
2. 确保Maven已安装
3. 检查端口8080是否被占用
4. 查看控制台日志输出

## 开发说明

这是一个最小化的Spring Boot项目，包含了：
- 主启动类
- 测试控制器
- 基本配置
- Maven构建配置

可以在此基础上扩展更多功能。
