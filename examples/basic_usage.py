#!/usr/bin/env python3
"""
快乐魔仙数字货币分析技能 - 基础使用示例
"""

import asyncio
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.main import HappyFairyCryptoAnalysis

async def main():
    """主函数示例"""
    print("🧚✨ 快乐魔仙数字货币分析技能 - 基础使用示例")
    print("=" * 50)
    
    # 1. 创建分析器实例
    print("1. 初始化分析系统...")
    analyzer = HappyFairyCryptoAnalysis()
    
    # 2. 初始化系统
    if not analyzer.initialize():
        print("❌ 系统初始化失败")
        return
    
    print("✅ 系统初始化成功")
    
    # 3. 分析BTC
    print("\n2. 分析BTC...")
    btc_result = await analyzer.analyze_currency("BTC")
    
    if 'error' in btc_result:
        print(f"❌ BTC分析失败: {btc_result['error']}")
    else:
        price = btc_result['price_data']['price']
        signal = btc_result['technical_analysis']['signals']['technical_signal']
        recommendation = btc_result['technical_analysis']['signals']['recommendation']
        
        print(f"✅ BTC分析成功:")
        print(f"   价格: ${price:,.2f}")
        print(f"   技术信号: {signal}")
        print(f"   操作建议: {recommendation}")
    
    # 4. 分析ETH
    print("\n3. 分析ETH...")
    eth_result = await analyzer.analyze_currency("ETH")
    
    if 'error' in eth_result:
        print(f"❌ ETH分析失败: {eth_result['error']}")
    else:
        price = eth_result['price_data']['price']
        signal = eth_result['technical_analysis']['signals']['technical_signal']
        recommendation = eth_result['technical_analysis']['signals']['recommendation']
        
        print(f"✅ ETH分析成功:")
        print(f"   价格: ${price:,.2f}")
        print(f"   技术信号: {signal}")
        print(f"   操作建议: {recommendation}")
    
    # 5. 打印控制台报告
    print("\n4. 打印完整分析报告...")
    analyzer.print_analysis_result(btc_result)
    analyzer.print_analysis_result(eth_result)
    
    print("\n🎉 示例完成！")
    print("=" * 50)
    print("🧚✨ 快乐魔仙数字货币分析技能 - 让分析更简单，让交易更智能！")

if __name__ == "__main__":
    asyncio.run(main())