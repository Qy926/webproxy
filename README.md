# WebProxy Service

企业级Web代理服务系统，提供用户策略管理、流量统计、计费查询等功能的REST API服务。

## 功能特性

- **用户策略查询**: 根据用户名获取企业策略信息
- **流量统计**: 支持用户级和组级的流量使用情况查询
- **计费查询**: 支持用户级和组级的计费使用情况查询
- **缓存机制**: 内置缓存优化，提高查询性能
- **链路追踪**: 支持完整的请求链路追踪
- **结构化日志**: 详细的日志记录和异常处理

## 系统架构

本系统采用微服务架构，通过多个服务组件协同工作：

```
WebProxy Service (主服务)
├── Domain Service    # 域名管理服务
├── User Service      # 用户管理服务
├── Policy Service    # 策略管理服务
├── Traffic Service   # 流量统计服务
├── Billing Service   # 计费服务
└── Cache Service     # 缓存服务
```

## 项目结构

```
webproxy/
├── webproxy.py          # 主服务入口，Flask应用
├── domainhandler.py     # 域名服务处理器
├── userhandler.py       # 用户服务处理器
├── policyhandler.py     # 策略服务处理器
├── traffichandler.py    # 流量服务处理器
├── billinghandler.py    # 计费服务处理器
├── cachehandler.py      # 缓存服务处理器
├── logging.ini          # 日志配置文件
└── README.md           # 项目说明文档
```

## 依赖要求

- Python 3.6+
- Flask 2.0+
- requests

## 安装和配置

### 1. 安装依赖

```bash
pip install flask requests
```

### 2. 环境配置

确保以下服务可访问：
- Domain Service: `domain.webproxy.com:8080`
- User Service: `user.webproxy.com:8080`
- Policy Service: `policy.webproxy.com:8080`
- Traffic Service: `traffic.webproxy.com:8080`
- Billing Service: `billing.webproxy.com:8080`
- Cache Service: `cache.webproxy.com:8080`

### 3. 日志配置

确保日志目录存在：
```bash
mkdir -p /var/log
```

## 启动服务

```bash
python webproxy.py
```

服务将在 `0.0.0.0:8080` 启动。

## API 接口

### 1. 获取用户策略

**接口**: `GET /api/v1/getpolicy`

**参数**:
- `username` (required): 用户邮箱地址

**示例**:
```bash
curl "http://localhost:8080/api/v1/getpolicy?username=user@company.com"
```

**响应**:
```json
{
  "policy": {
    "policyId": "123",
    "rules": [...]
  }
}
```

### 2. 获取用户流量使用情况

**接口**: `GET /api/v1/getusertrafficusage`

**参数**:
- `username` (required): 用户邮箱地址

**示例**:
```bash
curl "http://localhost:8080/api/v1/getusertrafficusage?username=user@company.com"
```

**响应**:
```json
{
  "traffic": {
    "companyTotalTraffic": 1000000,
    "userTotalTraffic": 50000,
    "usagePercentage": 5.0
  }
}
```

### 3. 获取组流量使用情况

**接口**: `GET /api/v1/getgrouptrafficusage`

**参数**:
- `companyid` (required): 企业ID
- `groupname` (required): 组名称

**示例**:
```bash
curl "http://localhost:8080/api/v1/getgrouptrafficusage?companyid=123&groupname=dev-team"
```

**响应**:
```json
{
  "traffic": {
    "companyTotalTraffic": 1000000,
    "groupTotalTraffic": 200000,
    "usagePercentage": 20.0
  }
}
```

### 4. 获取用户计费使用情况

**接口**: `GET /api/v1/getuserbillingusage`

**参数**:
- `username` (required): 用户邮箱地址

**示例**:
```bash
curl "http://localhost:8080/api/v1/getuserbillingusage?username=user@company.com"
```

**响应**:
```json
{
  "billing": {
    "companyBilling": 10000,
    "userBilling": 500,
    "usagePercentage": 5.0
  }
}
```

### 5. 获取组计费使用情况

**接口**: `GET /api/v1/getgroupbillingusage`

**参数**:
- `companyid` (required): 企业ID
- `groupname` (required): 组名称

**示例**:
```bash
curl "http://localhost:8080/api/v1/getgroupbillingusage?companyid=123&groupname=dev-team"
```

**响应**:
```json
{
  "billing": {
    "companyBilling": 10000,
    "groupBilling": 2000,
    "usagePercentage": 20.0
  }
}
```

## 错误处理

系统返回标准HTTP状态码：

- `200 OK`: 请求成功
- `400 Bad Request`: 请求参数无效
- `404 Not Found`: 用户、组或策略未找到
- `500 Internal Server Error`: 服务器内部错误

错误响应格式：
```json
{
  "error": "错误描述信息"
}
```

## 缓存策略

系统采用多级缓存策略优化性能：

- **长期缓存** (24小时): 域名到企业ID映射、用户ID映射
- **默认缓存** (2小时): 一般查询结果
- **短期缓存** (5分钟): 临时数据

## 监控和日志

### 日志配置
- 日志文件: `/var/log/webproxy.log`
- 轮转策略: 每日轮转，保留5天
- 日志级别: INFO

### 链路追踪
每个请求都会生成唯一的 `trace_id`，方便问题追踪和性能分析。

### 关键监控指标
- API响应时间
- 错误率
- 缓存命中率
- 依赖服务可用性

## 开发和维护

### 代码结构
- 每个服务处理器独立封装，便于单元测试
- 统一的错误处理和日志记录
- 支持超时配置和重试机制

### 扩展指南
1. 添加新的API接口：在 `webproxy.py` 中添加路由
2. 添加新的服务依赖：创建对应的handler类
3. 修改缓存策略：调整 `CacheHandler` 中的TTL配置

## 故障排查

### 常见问题

1. **服务无法启动**
   - 检查端口8080是否被占用
   - 确认依赖服务可访问

2. **API返回404错误**
   - 检查依赖服务是否正常运行
   - 验证请求参数格式

3. **响应缓慢**
   - 检查缓存服务状态
   - 查看依赖服务响应时间

### 日志分析
使用 `trace_id` 追踪完整请求链路：
```bash
grep "trace_id=xxx" /var/log/webproxy.log
```