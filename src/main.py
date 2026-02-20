#!/usr/bin/env python3
"""
快乐魔仙数字货币分析技能 - 主程序
入口点，提供CLI接口和监控服务
"""

import sys
import os
import asyncio
import logging
import argparse
from typing import Dict, Any, Optional
from datetime import datetime

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.loader import ConfigLoader
from src.api.coingecko import CoinGeckoClient
from src.analysis.indicators import TechnicalIndicators
from src.notification.telegram import NotificationManager

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('happy_fairy_analysis.log')
    ]
)

logger = logging.getLogger(__name__)

class HappyFairyCryptoAnalysis:
    """快乐魔仙数字货币分析主类"""
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化分析系统"""
        self.config_path = config_path
        self.config = None
        self.config_loader = None
        self.api_client = None
        self.indicators = None
        self.notification_manager = None
        self.monitoring_task = None
        self.running = False
        
        logger.info("🧚✨ 快乐魔仙数字货币分析系统初始化")
    
    def initialize(self):
        """初始化所有组件"""
        try:
            # 1. 加载配置
            self.config_loader = ConfigLoader(self.config_path)
            self.config = self.config_loader.load()
            logger.info("配置加载完成")
            
            # 2. 初始化API客户端
            api_config = self.config.get('api', {}).get('coingecko', {})
            self.api_client = CoinGeckoClient(
                api_key=api_config.get('api_key'),
                cache_ttl=api_config.get('cache_ttl', 300)
            )
            logger.info("API客户端初始化完成")
            
            # 3. 初始化技术指标引擎
            analysis_config = self.config.get('analysis', {})
            indicators_config = analysis_config.get('indicators', {})
            
            # 转换配置格式
            tech_config = {
                'ma_periods': indicators_config.get('ma', {}).get('periods', [5, 48, 180]),
                'macd_params': [
                    indicators_config.get('macd', {}).get('fast', 6),
                    indicators_config.get('macd', {}).get('slow', 7),
                    indicators_config.get('macd', {}).get('signal', 6)
                ],
                'kdj_params': [
                    indicators_config.get('kdj', {}).get('period', 9),
                    indicators_config.get('kdj', {}).get('k_period', 3),
                    indicators_config.get('kdj', {}).get('d_period', 3)
                ],
                'skdj_params': [
                    indicators_config.get('skdj', {}).get('period', 9),
                    indicators_config.get('skdj', {}).get('k_period', 3),
                    indicators_config.get('skdj', {}).get('d_period', 3)
                ],
                'obv_period': indicators_config.get('obv', {}).get('period', 30),
                'td_markers': [
                    indicators_config.get('td', {}).get('buy_count', 9),
                    indicators_config.get('td', {}).get('sell_count', 13)
                ]
            }
            
            self.indicators = TechnicalIndicators(tech_config)
            logger.info("技术指标引擎初始化完成")
            
            # 4. 初始化通知管理器
            self.notification_manager = NotificationManager(self.config)
            logger.info("通知管理器初始化完成")
            
            logger.info("✅ 系统初始化完成")
            return True
            
        except Exception as e:
            logger.error(f"系统初始化失败: {e}")
            return False
    
    async def analyze_currency(self, currency_symbol: str) -> Dict[str, Any]:
        """分析指定币种"""
        try:
            # 获取币种配置
            currency_config = self.config_loader.get_currency_config(currency_symbol)
            if not currency_config:
                return {'error': f'未找到币种配置: {currency_symbol}'}
            
            coin_id = currency_config.get('coin_id')
            currency_name = currency_config.get('name', currency_symbol)
            
            logger.info(f"开始分析 {currency_name} ({currency_symbol})")
            
            # 1. 获取当前价格
            price_data = self.api_client.get_price(coin_id)
            if 'error' in price_data:
                return {'error': f'获取价格失败: {price_data["error"]}'}
            
            # 2. 获取市场数据（用于技术分析）
            market_data = self.api_client.get_market_data(coin_id, days=7)
            if 'error' in market_data:
                return {'error': f'获取市场数据失败: {market_data["error"]}'}
            
            # 3. 技术指标分析
            analysis_result = self.indicators.analyze_all_indicators(market_data)
            if 'error' in analysis_result:
                return {'error': f'技术分析失败: {analysis_result["error"]}'}
            
            # 4. 合并结果
            result = {
                'currency': currency_symbol,
                'name': currency_name,
                'coin_id': coin_id,
                'price_data': price_data,
                'market_data': market_data,
                'technical_analysis': analysis_result,
                'analysis_time': datetime.now().isoformat(),
                'success': True
            }
            
            logger.info(f"{currency_name} 分析完成: {analysis_result.get('signals', {}).get('technical_signal', '未知')}")
            return result
            
        except Exception as e:
            logger.error(f"分析 {currency_symbol} 失败: {e}")
            return {'error': f'分析失败: {str(e)}', 'success': False}
    
    async def analyze_all_currencies(self) -> Dict[str, Dict[str, Any]]:
        """分析所有启用的币种"""
        results = {}
        enabled_currencies = self.config_loader.get_enabled_currencies()
        
        logger.info(f"开始分析 {len(enabled_currencies)} 个币种")
        
        for currency in enabled_currencies:
            symbol = currency.get('symbol')
            result = await self.analyze_currency(symbol)
            results[symbol] = result
            
            # 短暂延迟，避免API限制
            await asyncio.sleep(1)
        
        logger.info(f"所有币种分析完成")
        return results
    
    async def send_analysis_report(self, currency_symbol: str, analysis_result: Dict[str, Any]) -> bool:
        """发送分析报告"""
        try:
            if not self.notification_manager:
                logger.warning("通知管理器未初始化，跳过发送报告")
                return False
            
            # 检查是否应该发送通知
            if not self.notification_manager.should_send_notification(currency_symbol, 'analysis_report'):
                logger.debug(f"{currency_symbol} 分析报告在冷却中，跳过发送")
                return False
            
            # 发送分析报告
            send_results = await self.notification_manager.send_analysis_report(
                currency_symbol, 
                analysis_result.get('technical_analysis', {})
            )
            
            success = any(send_results.values())
            if success:
                logger.info(f"{currency_symbol} 分析报告发送成功")
            else:
                logger.warning(f"{currency_symbol} 分析报告发送失败")
            
            return success
            
        except Exception as e:
            logger.error(f"发送分析报告失败: {e}")
            return False
    
    async def monitor_currencies(self):
        """监控币种（后台任务）"""
        logger.info("开始监控币种")
        self.running = True
        
        check_interval = self.config.get('monitoring', {}).get('check_interval', 60)
        alert_threshold = self.config.get('monitoring', {}).get('alert_threshold', 1.0)
        
        # 存储上次价格，用于计算变化
        last_prices = {}
        
        while self.running:
            try:
                enabled_currencies = self.config_loader.get_enabled_currencies()
                
                for currency in enabled_currencies:
                    symbol = currency.get('symbol')
                    coin_id = currency.get('coin_id')
                    
                    # 获取当前价格
                    price_data = self.api_client.get_price(coin_id)
                    if 'error' in price_data:
                        logger.error(f"获取 {symbol} 价格失败: {price_data['error']}")
                        continue
                    
                    current_price = price_data.get('price', 0)
                    last_price = last_prices.get(symbol)
                    
                    # 检查价格突变
                    if last_price and current_price > 0:
                        price_change = abs((current_price - last_price) / last_price) * 100
                        
                        if price_change >= alert_threshold:
                            logger.info(f"{symbol} 价格突变: {price_change:.2f}%")
                            
                            # 发送价格警报
                            if self.notification_manager:
                                await self.notification_manager.send_price_alert(symbol, price_data)
                    
                    # 更新上次价格
                    last_prices[symbol] = current_price
                    
                    # 分析并发送报告
                    analysis_result = await self.analyze_currency(symbol)
                    if analysis_result.get('success', False):
                        await self.send_analysis_report(symbol, analysis_result)
                    
                    # 短暂延迟
                    await asyncio.sleep(2)
                
                # 等待下一次检查
                logger.debug(f"监控循环完成，等待 {check_interval} 秒")
                await asyncio.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"监控循环出错: {e}")
                await asyncio.sleep(10)  # 出错后等待更长时间
    
    async def start_monitoring(self):
        """启动监控服务"""
        if self.monitoring_task and not self.monitoring_task.done():
            logger.warning("监控服务已经在运行")
            return False
        
        try:
            # 初始化通知管理器（异步）
            await self.notification_manager.initialize_all()
            
            # 测试通知连接
            test_results = await self.notification_manager.test_all_connections()
            if any(test_results.values()):
                logger.info("通知连接测试成功")
            else:
                logger.warning("通知连接测试失败，继续运行但不发送通知")
            
            # 启动监控任务
            self.monitoring_task = asyncio.create_task(self.monitor_currencies())
            logger.info("监控服务已启动")
            return True
            
        except Exception as e:
            logger.error(f"启动监控服务失败: {e}")
            return False
    
    async def stop_monitoring(self):
        """停止监控服务"""
        self.running = False
        
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
            
            self.monitoring_task = None
        
        # 关闭通知管理器
        if self.notification_manager:
            self.notification_manager.shutdown()
        
        logger.info("监控服务已停止")
    
    def print_analysis_result(self, result: Dict[str, Any]):
        """打印分析结果到控制台"""
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
            return
        
        currency = result.get('currency', '未知')
        name = result.get('name', currency)
        price_data = result.get('price_data', {})
        analysis = result.get('technical_analysis', {})
        signals = analysis.get('signals', {})
        
        current_price = price_data.get('price', 0)
        change_24h = price_data.get('change_24h', 0)
        signal = signals.get('technical_signal', '未知')
        recommendation = signals.get('recommendation', '持有')
        reason = signals.get('reason', '')
        
        print(f"\n{'='*50}")
        print(f"📊 {name} ({currency}) 分析报告")
        print(f"{'='*50}")
        print(f"💰 当前价格: ${current_price:,.2f}")
        
        if change_24h > 0:
            print(f"📈 24小时变化: +{change_24h:.2f}%")
        else:
            print(f"📉 24小时变化: {change_24h:.2f}%")
        
        print(f"🎯 技术信号: {signal}")
        print(f"💡 操作建议: {recommendation}")
        print(f"📝 分析依据: {reason}")
        print(f"⏰ 分析时间: {result.get('analysis_time', '')}")
        print(f"{'='*50}")
        print("⚠️  风险提示: 仅供参考，不构成交易依据。")
        print(f"{'='*50}\n")


async def main_async():
    """异步主函数"""
    parser = argparse.ArgumentParser(description='快乐魔仙数字货币分析技能')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--analyze', '-a', help='分析指定币种 (如: BTC, ETH)')
    parser.add_argument('--analyze-all', action='store_true', help='分析所有启用的币种')
    parser.add_argument('--monitor', '-m', action='store_true', help='启动监控服务')
    parser.add_argument('--stop', '-s', action='store_true', help='停止监控服务')
    parser.add_argument('--test', '-t', action='store_true', help='测试系统功能')
    parser.add_argument('--version', '-v', action='store_true', help='显示版本信息')
    
    args = parser.parse_args()
    
    # 显示版本信息
    if args.version:
        print("🧚✨ 快乐魔仙数字货币分析技能 v1.0.0")
        print("作者: 快乐魔仙 🧚✨ & 黎山 🌄")
        print("许可证: MIT")
        return
    
    # 创建分析系统实例
    analyzer = HappyFairyCryptoAnalysis(args.config)
    
    if not analyzer.initialize():
        print("❌ 系统初始化失败，请检查配置和依赖")
        return
    
    try:
        if args.test:
            # 测试系统功能
            print("🧪 测试系统功能...")
            
            # 测试API连接
            api_status = analyzer.api_client.check_api_status()
            print(f"📡 API状态: {api_status.get('status', '未知')}")
            
            # 测试通知连接
            if analyzer.notification_manager:
                test_results = await analyzer.notification_manager.test_all_connections()
                for name, success in test_results.items():
                    status = "✅ 成功" if success else "❌ 失败"
                    print(f"📱 {name}通知: {status}")
            
            print("✅ 系统测试完成")
            
        elif args.analyze:
            # 分析指定币种
            result = await analyzer.analyze_currency(args.analyze.upper())
            analyzer.print_analysis_result(result)
            
            # 发送通知
            if result.get('success', False):
                await analyzer.send_analysis_report(args.analyze.upper(), result)
        
        elif args.analyze_all:
            # 分析所有币种
            results = await analyzer.analyze_all_currencies()
            for symbol, result in results.items():
                analyzer.print_analysis_result(result)
        
        elif args.monitor:
            # 启动监控服务
            print("🚀 启动监控服务...")
            success = await analyzer.start_monitoring()
            
            if success:
                print("✅ 监控服务已启动")
                print("📱 通知已启用")
                print("⏰ 按 Ctrl+C 停止监控")
                
                try:
                    # 保持运行
                    while analyzer.running:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    print("\n🛑 收到停止信号")
            else:
                print("❌ 启动监控服务失败")
            
            # 停止监控
            await analyzer.stop_monitoring()
            print("✅ 监控服务已停止")
        
        elif args.stop:
            #