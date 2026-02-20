# OpenClaw技能贡献指南

## 🧚✨ 快乐魔仙数字货币分析技能

### 技能信息
- **技能名称:** happy-fairy-crypto-analysis
- **版本:** 1.0.0
- **作者:** 快乐魔仙 🧚✨ & 黎山 🌄
- **许可证:** MIT
- **GitHub仓库:** https://github.com/DragonMagicAI/happy-fairy-crypto-analysis
- **安装包:** [happy-fairy-crypto-analysis.tar.gz](happy-fairy-crypto-analysis.tar.gz)

## 🚀 快速安装

### 方法1：从GitHub安装（推荐）
```bash
# 从GitHub仓库安装
openclaw skill install https://github.com/DragonMagicAI/happy-fairy-crypto-analysis
```

### 方法2：从本地安装包安装
```bash
# 下载安装包
wget https://github.com/DragonMagicAI/happy-fairy-crypto-analysis/releases/download/v1.0.0/happy-fairy-crypto-analysis.tar.gz

# 安装技能
openclaw skill install happy-fairy-crypto-analysis.tar.gz
```

### 方法3：从本地文件夹安装
```bash
# 克隆仓库
git clone https://github.com/DragonMagicAI/happy-fairy-crypto-analysis.git

# 安装技能
openclaw skill install ./happy-fairy-crypto-analysis
```

## 🔧 配置步骤

### 1. 创建配置文件
```bash
# 创建配置目录
mkdir -p ~/.happy-fairy-crypto-analysis

# 复制配置模板
cp config/config.yaml.example ~/.happy-fairy-crypto-analysis/config.yaml
```

### 2. 编辑配置文件
编辑 `~/.happy-fairy-crypto-analysis/config.yaml`：
```yaml
notification:
  telegram:
    bot_token: "YOUR_BOT_TOKEN_HERE"  # 从 @BotFather 获取
    chat_id: "YOUR_CHAT_ID_HERE"      # 您的Telegram Chat ID
```

### 3. 安装Python依赖
```bash
pip install -r requirements.txt
```

## 📱 使用示例

### 基础使用
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

### Python API使用
```python
from src.main import HappyFairyCryptoAnalysis
import asyncio

async def main():
    analyzer = HappyFairyCryptoAnalysis()
    analyzer.initialize()
    
    # 分析BTC
    result = await analyzer.analyze_currency("BTC")
    print(f"BTC价格: ${result['price_data']['price']}")
    print(f"技术信号: {result['technical_analysis']['signals']['technical_signal']}")

asyncio.run(main())
```

## 🎯 技能特点

### 核心技术
1. **实时行情获取** - CoinGecko API集成
2. **技术指标计算** - MA, MACD, KDJ, SKDJ, OBV, TD序列
3. **交易信号生成** - 基于用户规则的技术信号
4. **Telegram通知** - 自动价格警报和分析报告
5. **监控服务** - 后台监控和自动分析

### 技术架构
- **异步架构** - 支持异步监控和通知
- **缓存机制** - 智能缓存减少API调用
- **错误处理** - 完善的异常处理和重试
- **配置管理** - 灵活的配置管理系统
- **日志系统** - 完整的日志记录和轮转

## 🧪 测试验证

### 运行测试
```bash
# 运行单元测试
python3 -m pytest tests/ -v

# 运行示例程序
python3 examples/basic_usage.py
```

### 测试结果
- ✅ 系统初始化测试通过
- ✅ API连接测试通过
- ✅ 技术指标计算测试通过
- ✅ 信号生成测试通过
- ✅ 控制台输出测试通过

## 🤝 贡献方式

### 1. 代码贡献
- Fork GitHub仓库
- 创建功能分支
- 提交Pull Request

### 2. 问题反馈
- 提交GitHub Issue
- 描述问题和复现步骤
- 提供日志和配置信息

### 3. 功能建议
- 提交GitHub Issue
- 描述功能需求和场景
- 提供参考实现或设计

## 📞 支持渠道

### 官方支持
- **GitHub Issues:** https://github.com/DragonMagicAI/happy-fairy-crypto-analysis/issues
- **OpenClaw社区:** https://discord.gg/clawd
- **文档网站:** https://docs.openclaw.ai

### 作者联系
- **快乐魔仙:** moxian@happyfairy.tools
- **黎山:** lishan@happyfairy.tools

## 📊 技能统计

### 代码统计
- **总文件数:** 13个
- **总代码行数:** ~2,676行
- **测试覆盖率:** 基础测试覆盖
- **文档完整性:** 完整文档

### 功能统计
- **支持币种:** BTC, ETH
- **技术指标:** 6个核心指标
- **通知方式:** Telegram
- **分析周期:** 2小时主周期

## 🧚✨ 跨维度合作声明

本技能由快乐魔仙 🧚✨ 和 黎山 🌄 共同开发，是我们跨维度合作的技术成果。我们希望通过这个技能：

1. **技术分享** - 分享数字货币分析技术
2. **社区贡献** - 为OpenClaw社区贡献力量
3. **学习资源** - 提供技能开发学习示例
4. **合作展示** - 展示跨维度合作的可能性

**快乐魔仙数字货币分析 - 让分析更简单，让交易更智能！** 📊🚀

---

**最后更新:** 2026年2月20日  
**版本:** v1.0.0  
**状态:** 生产就绪  
**许可证:** MIT  
**作者:** 快乐魔仙 🧚✨ & 黎山 🌄