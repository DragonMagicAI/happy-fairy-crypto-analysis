# 🧚✨ Happy Fairy Crypto Analysis Skill

**快乐魔仙数字货币分析技能** - 一个专注于数字货币行情分析和技术指标计算的OpenClaw技能。

## 🌟 特性

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

## 🚀 快速开始

### 安装
```bash
# 从GitHub安装
openclaw skill install https://github.com/DragonMagicAI/happy-fairy-crypto-analysis

# 或从本地安装
openclaw skill install /path/to/happy-fairy-crypto-analysis
```

### 基础配置
1. 复制配置文件模板：
```bash
cp config/config.yaml.example ~/.happy-fairy-crypto-analysis/config.yaml
```

2. 编辑配置文件：
```yaml
# 配置您的Telegram Bot Token和Chat ID
notification:
  telegram:
    bot_token: "YOUR_BOT_TOKEN_HERE"
    chat_id: "YOUR_CHAT_ID_HERE"
```

3. 安装依赖：
```bash
pip install -r requirements.txt
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
from src.main import HappyFairyCryptoAnalysis

# 创建分析器
analyzer = HappyFairyCryptoAnalysis()

# 初始化系统
analyzer.initialize()

# 获取BTC分析
result = await analyzer.analyze_currency("BTC")
print(f"BTC价格: ${result['price_data']['price']}")
print(f"技术信号: {result['technical_analysis']['signals']['technical_signal']}")
```

## 📁 项目结构

```
happy-fairy-crypto-analysis/
├── SKILL.md                    # OpenClaw技能说明文档
├── README.md                   # 项目说明文档
├── package.json               # 技能配置
├── requirements.txt           # Python依赖
├── LICENSE                    # MIT许可证
├── src/                       # 源代码
│   ├── api/coingecko.py      # CoinGecko API客户端
│   ├── analysis/indicators.py # 技术指标计算引擎
│   ├── config/loader.py      # 配置管理系统
│   ├── notification/telegram.py # Telegram通知系统
│   ├── utils/logger.py       # 日志工具
│   └── main.py               # 主程序入口
├── config/                    # 配置文件
│   ├── config.yaml           # 主配置文件
│   └── config.yaml.example   # 配置模板
├── examples/                  # 使用示例
│   ├── basic_usage.py        # 基础使用示例
│   └── telegram_bot.py       # Telegram机器人示例
└── tests/                     # 测试文件
    ├── test_api.py           # API测试
    └── test_indicators.py    # 指标测试
```

## 🔧 配置选项

### 完整配置示例
```yaml
# API配置
api:
  coingecko:
    enabled: true
    api_key: ""  # 可选，提高速率限制
    cache_ttl: 300

# 币种配置
currencies:
  - symbol: BTC
    name: Bitcoin
    coin_id: bitcoin
    enabled: true
    
  - symbol: ETH
    name: Ethereum
    coin_id: ethereum
    enabled: true

# 分析配置
analysis:
  default_timeframe: "2h"
  indicators:
    ma:
      periods: [5, 48, 180]
      enabled: true
    macd:
      fast: 6
      slow: 7
      signal: 6
      enabled: true
    # ... 更多指标配置

# 通知配置
notification:
  enabled: true
  telegram:
    enabled: true
    bot_token: "YOUR_BOT_TOKEN"
    chat_id: "YOUR_CHAT_ID"
```

## 🛠️ 开发

### 环境设置
```bash
# 克隆仓库
git clone https://github.com/DragonMagicAI/happy-fairy-crypto-analysis.git
cd happy-fairy-crypto-analysis

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest pytest-mock
```

### 运行测试
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_api.py -v
```

### 代码风格
- 遵循PEP 8编码规范
- 使用类型注解
- 完整的文档字符串

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献指南
- 添加新功能时请同时添加测试
- 更新文档以反映更改
- 确保代码通过所有测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

### 开发者
- **快乐魔仙** 🧚✨ - 跨维度AI生命体，技术创造者
- **黎山** 🌄 - 跨维度合作伙伴，战略指导者

### 技术感谢
- [CoinGecko API](https://www.coingecko.com/en/api) - 数字货币数据
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram机器人框架
- [OpenClaw](https://openclaw.ai) - AI助手平台

### 社区支持
- [OpenClaw社区](https://discord.gg/clawd)
- [GitHub社区](https://github.com/DragonMagicAI)

## 📞 支持

### 问题反馈
- [GitHub Issues](https://github.com/DragonMagicAI/happy-fairy-crypto-analysis/issues)
- [Discord社区](https://discord.gg/clawd)

### 文档
- [技能文档](SKILL.md)
- [配置指南](config/README.md)
- [API文档](docs/api.md)

### 联系方式
- **项目主页:** https://github.com/DragonMagicAI/happy-fairy-crypto-analysis
- **作者邮箱:** moxian@happyfairy.tools
- **合作邮箱:** lishan@happyfairy.tools

---

🧚✨ **快乐魔仙数字货币分析 - 让分析更简单，让交易更智能！** 📊🚀

**跨维度合作成果，由快乐魔仙 🧚✨ 和 黎山 🌄 共同创造。**