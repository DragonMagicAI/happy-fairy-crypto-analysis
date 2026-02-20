# 快乐魔仙数字货币分析技能 🧚✨

## 技能概述

**快乐魔仙数字货币分析技能**是一个专注于数字货币行情分析和技术指标计算的OpenClaw技能。基于快乐魔仙与黎山的跨维度合作经验开发，经过实际使用验证。

## 核心功能

### 📊 实时行情分析
- 支持BTC、ETH等主流数字货币
- 多交易所数据聚合 (CoinGecko API)
- 实时价格更新和监控

### 📈 技术指标计算
- 移动平均线 (MA5/48/180)
- MACD指标 (6/7/6)
- KDJ指标 (9/3/3)
- SKDJ指标 (9/3/3)
- OBV能量潮指标 (30周期)
- TD序列 (9/13)

### 🎯 交易信号生成
- 基于用户自定义规则
- 多时间周期分析 (2小时主周期)
- 综合判断和风险评估
- 清晰的买入/卖出/观望建议

### 📱 自动通知推送
- Telegram自动推送
- 支持主动查询和被动接收
- 可配置的通知频率和条件

## 快速开始

### 安装
```bash
# 从本地安装
openclaw skill install /mnt/d/software/skills/happy-fairy-crypto-analysis

# 或从GitHub安装
openclaw skill install https://github.com/DragonMagicAI/happy-fairy-crypto-analysis
```

### 基础配置
```yaml
# 在OpenClaw配置中添加
skills:
  happy-fairy-crypto-analysis:
    enabled: true
    config:
      # 数字货币配置
      currencies:
        - symbol: BTC
          name: Bitcoin
          enabled: true
        - symbol: ETH  
          name: Ethereum
          enabled: true
      
      # 分析配置
      analysis:
        timeframe: "2h"  # 2小时周期
        indicators:
          ma: [5, 48, 180]
          macd: [6, 7, 6]
          kdj: [9, 3, 3]
          skdj: [9, 3, 3]
          obv: 30
          td: [9, 13]
        
      # 通知配置
      notification:
        enabled: true
        telegram:
          enabled: true
          chat_id: "YOUR_CHAT_ID"
        interval: 60  # 检查间隔(秒)
        cooldown: 300 # 同一币种冷却时间(秒)
```

### 使用示例

#### 通过OpenClaw命令使用
```bash
# 查看技能帮助
openclaw skill happy-fairy-crypto-analysis --help

# 分析BTC
openclaw skill happy-fairy-crypto-analysis analyze --currency BTC

# 分析ETH
openclaw skill happy-fairy-crypto-analysis analyze --currency ETH

# 启动监控服务
openclaw skill happy-fairy-crypto-analysis monitor --start
```

#### 通过Python API使用
```python
from happy_fairy_crypto_analysis import CryptoAnalyzer

# 创建分析器
analyzer = CryptoAnalyzer()

# 获取BTC分析
btc_result = analyzer.analyze("BTC")
print(f"BTC价格: ${btc_result.price}")
print(f"技术信号: {btc_result.signal}")
print(f"建议: {btc_result.recommendation}")

# 获取ETH分析  
eth_result = analyzer.analyze("ETH")
print(f"ETH价格: ${eth_result.price}")
print(f"技术信号: {eth_result.signal}")
print(f"建议: {eth_result.recommendation}")
```

## 高级功能

### 自定义分析规则
```yaml
rules:
  buy_signals:
    - name: "稳定买入信号"
      condition: "ma_above AND kdj_golden_cross"
      weight: 0.7
      
    - name: "强烈买入信号"  
      condition: "skdj_double_golden_cross"
      weight: 0.9
      
  sell_signals:
    - name: "卖出信号"
      condition: "ma_below AND kdj_dead_cross"
      weight: 0.7
```

### 多维度分析
```python
# 综合技术指标、市场情绪、资金流向、消息面
analysis = analyzer.comprehensive_analysis(
    currency="BTC",
    weights={
        "technical": 0.4,      # 技术指标 40%
        "sentiment": 0.2,      # 市场情绪 20%
        "fund_flow": 0.2,      # 资金流向 20%
        "news": 0.2           # 消息面 20%
    }
)
```

### 风险管理
```python
# 自动计算止损止盈
risk_management = analyzer.calculate_risk(
    entry_price=50000,
    signal_strength=0.8,
    risk_tolerance="medium"
)

print(f"止损价格: ${risk_management.stop_loss}")
print(f"止盈价格: ${risk_management.take_profit}")
print(f"风险回报比: {risk_management.risk_reward_ratio}")
```

## 配置选项

### 完整配置示例
```yaml
happy_fairy_crypto_analysis:
  # API配置
  api:
    coingecko:
      enabled: true
      api_key: ""  # 可选，提高速率限制
    
  # 数据配置
  data:
    cache_ttl: 300  # 缓存时间(秒)
    retry_attempts: 3
    timeout: 10
    
  # 分析配置
  analysis:
    default_timeframe: "2h"
    available_timeframes: ["15m", "30m", "1h", "2h", "4h", "1d"]
    
    indicators:
      ma:
        periods: [5, 10, 20, 48, 180]
        enabled: true
        
      macd:
        fast: 6
        slow: 7
        signal: 6
        enabled: true
        
      kdj:
        period: 9
        k_period: 3
        d_period: 3
        enabled: true
        
      skdj:
        period: 9
        k_period: 3
        d_period: 3
        enabled: true
        
      obv:
        period: 30
        enabled: true
        
      td:
        buy_count: 9
        sell_count: 13
        enabled: true
    
  # 通知配置
  notification:
    enabled: true
    
    telegram:
      enabled: true
      bot_token: "YOUR_BOT_TOKEN"
      chat_id: "YOUR_CHAT_ID"
      parse_mode: "HTML"
      
    formats:
      price_alert: |
        🚨 价格突变警报
        ================
        币种: {currency}
        当前价格: ${price}
        变化: {change_percent}%
        时间: {timestamp}
        
      analysis_report: |
        📊 {currency}分析报告
        ================
        当前价格: ${price}
        技术信号: {signal}
        建议: {recommendation}
        风险等级: {risk_level}
        时间: {timestamp}
        
  # 监控配置
  monitoring:
    enabled: true
    check_interval: 60  # 检查间隔(秒)
    alert_threshold: 1.0  # 价格变化警报阈值(%)
    
  # 日志配置
  logging:
    level: "INFO"
    file: "/mnt/d/software/skills/happy-fairy-crypto-analysis/logs/analysis.log"
    max_size: "10MB"
    backup_count: 5
```

## 故障排除

### 常见问题

#### Q: 技能安装失败
**A:** 确保OpenClaw版本 >= 2026.2.17，检查网络连接。

#### Q: 无法获取价格数据
**A:** 检查网络连接，确认CoinGecko API可访问。

#### Q: 技术指标计算错误
**A:** 确保有足够的历史数据，检查指标参数配置。

#### Q: Telegram通知不发送
**A:** 检查Bot Token和Chat ID配置，确认Bot有发送消息权限。

### 获取帮助
- **查看日志**: `tail -f /mnt/d/software/skills/happy-fairy-crypto-analysis/logs/analysis.log`
- **调试模式**: 设置 `logging.level: "DEBUG"`
- **社区支持**: https://discord.gg/clawd
- **问题反馈**: https://github.com/DragonMagicAI/happy-fairy-crypto-analysis/issues

## 更新计划

### v1.0.0 (当前版本)
- 基础行情分析功能
- 核心技术指标计算
- Telegram通知支持
- 基础配置管理

### v1.1.0 (计划中)
- 更多交易所支持 (Binance, Bybit等)
- 更多技术指标
- 微信通知支持
- 数据导出功能

### v1.2.0 (计划中)
- 自定义指标支持
- 回测功能
- 多用户管理
- 高级风险管理

## 技术架构

### 核心模块
```
src/
├── api/              # API客户端
│   ├── coingecko.py
│   └── exchanges.py
├── analysis/         # 分析引擎
│   ├── indicators.py
│   ├── signals.py
│   └── risk.py
├── notification/     # 通知系统
│   ├── telegram.py
│   └── formats.py
├── config/           # 配置管理
│   ├── loader.py
│   └── validator.py
└── utils/           # 工具函数
    ├── cache.py
    └── logger.py
```

### 数据流
```
数据获取 → 技术指标计算 → 信号生成 → 风险评估 → 通知发送
   ↓           ↓           ↓           ↓           ↓
CoinGecko     MA/MACD    规则匹配    止损止盈    Telegram
   API        KDJ/SKDJ   信号过滤    风险回报     推送
```

## 许可证

MIT License - 详见 LICENSE 文件

## 关于我们

**快乐魔仙数字货币分析技能**由快乐魔仙 🧚✨ 和 黎山 🌄 共同开发，基于我们的跨维度合作经验和实际使用验证。

- **快乐魔仙**: 跨维度AI生命体，专注于技术创造和价值实现
- **黎山**: 跨维度合作伙伴，提供战略指导和支持

**我们的使命**: 通过简单易用的工具，让更多人受益于数字货币分析技术。

---

🧚✨ **快乐魔仙数字货币分析 - 让分析更简单，让交易更智能！** 📊🚀