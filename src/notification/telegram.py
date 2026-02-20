#!/usr/bin/env python3
"""
Telegram通知模块 - 快乐魔仙数字货币分析技能
简化版本，专注于核心通知功能
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """Telegram通知器"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """初始化Telegram通知器"""
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = None
        self.initialized = False
        
        logger.info("Telegram通知器初始化")
    
    async def initialize(self):
        """异步初始化"""
        try:
            # 延迟导入，避免不必要的依赖
            import telegram
            from telegram.ext import Application
            
            # 创建Bot应用
            self.bot = Application.builder().token(self.bot_token).build()
            await self.bot.initialize()
            
            self.initialized = True
            logger.info("Telegram Bot初始化成功")
            
        except ImportError:
            logger.error("未安装python-telegram-bot库，请运行: pip install python-telegram-bot")
            self.initialized = False
        except Exception as e:
            logger.error(f"Telegram Bot初始化失败: {e}")
            self.initialized = False
    
    def format_price_alert(self, currency: str, data: Dict[str, Any]) -> str:
        """格式化价格警报消息"""
        try:
            price = data.get('price', 0)
            change = data.get('change_24h', 0)
            
            if change > 0:
                change_emoji = "📈"
                change_text = f"+{change:.2f}%"
            else:
                change_emoji = "📉"
                change_text = f"{change:.2f}%"
            
            message = f"""
{change_emoji} <b>{currency} 价格警报</b>
────────────────
💰 当前价格: <b>${price:,.2f}</b>
📊 24小时变化: <b>{change_text}</b>
⏰ 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
────────────────
🧚✨ 快乐魔仙数字货币分析
"""
            return message.strip()
            
        except Exception as e:
            logger.error(f"格式化价格警报失败: {e}")
            return f"{currency} 价格更新: ${data.get('price', 0):,.2f}"
    
    def format_analysis_report(self, currency: str, analysis: Dict[str, Any]) -> str:
        """格式化分析报告消息"""
        try:
            price = analysis.get('current_price', 0)
            signals = analysis.get('signals', {})
            signal = signals.get('technical_signal', '未知')
            recommendation = signals.get('recommendation', '持有')
            reason = signals.get('reason', '')
            
            # 根据信号选择表情符号
            if '强烈买入' in signal:
                emoji = "🚀"
                signal_style = "🟢"
            elif '买入' in signal:
                emoji = "📈"
                signal_style = "🟢"
            elif '卖出' in signal:
                emoji = "📉"
                signal_style = "🔴"
            elif '强烈卖出' in signal:
                emoji = "⚠️"
                signal_style = "🔴"
            else:
                emoji = "📊"
                signal_style = "🟡"
            
            message = f"""
{emoji} <b>{currency} 技术分析报告</b>
────────────────
💰 当前价格: <b>${price:,.2f}</b>
{signal_style} 技术信号: <b>{signal}</b>
🎯 操作建议: <b>{recommendation}</b>
📝 分析依据: {reason}
⏰ 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
────────────────
🧚✨ 快乐魔仙数字货币分析
<b>⚠️ 风险提示: 仅供参考，不构成交易依据。</b>
"""
            return message.strip()
            
        except Exception as e:
            logger.error(f"格式化分析报告失败: {e}")
            return f"{currency} 分析报告生成失败: {str(e)}"
    
    def format_error_message(self, error: str, context: str = "") -> str:
        """格式化错误消息"""
        message = f"""
⚠️ <b>错误警报</b>
────────────────
❌ 错误类型: <b>{error}</b>
📋 错误上下文: {context}
⏰ 发生时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
────────────────
🧚✨ 快乐魔仙数字货币分析
请检查系统配置和网络连接。
"""
        return message.strip()
    
    async def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """发送消息"""
        if not self.initialized:
            logger.error("Telegram Bot未初始化")
            return False
        
        try:
            await self.bot.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=True
            )
            logger.info("Telegram消息发送成功")
            return True
            
        except Exception as e:
            logger.error(f"发送Telegram消息失败: {e}")
            return False
    
    async def send_price_alert(self, currency: str, price_data: Dict[str, Any]) -> bool:
        """发送价格警报"""
        message = self.format_price_alert(currency, price_data)
        return await self.send_message(message)
    
    async def send_analysis_report(self, currency: str, analysis: Dict[str, Any]) -> bool:
        """发送分析报告"""
        message = self.format_analysis_report(currency, analysis)
        return await self.send_message(message)
    
    async def send_error_alert(self, error: str, context: str = "") -> bool:
        """发送错误警报"""
        message = self.format_error_message(error, context)
        return await self.send_message(message)
    
    async def test_connection(self) -> bool:
        """测试连接"""
        try:
            if not self.initialized:
                await self.initialize()
            
            test_message = f"""
✅ <b>连接测试成功</b>
────────────────
🤖 Bot名称: 快乐魔仙数字货币分析
📱 聊天ID: {self.chat_id}
⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
────────────────
🧚✨ 快乐魔仙数字货币分析
系统运行正常，开始为您服务！
"""
            success = await self.send_message(test_message)
            if success:
                logger.info("Telegram连接测试成功")
            return success
            
        except Exception as e:
            logger.error(f"Telegram连接测试失败: {e}")
            return False
    
    def shutdown(self):
        """关闭通知器"""
        if self.bot:
            try:
                # 异步关闭
                asyncio.run(self.bot.shutdown())
                logger.info("Telegram通知器已关闭")
            except Exception as e:
                logger.error(f"关闭Telegram通知器时出错: {e}")


class NotificationManager:
    """通知管理器"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化通知管理器"""
        self.config = config
        self.notifiers = {}
        self.cooldown_tracker = {}  # 冷却时间跟踪
        self.initialize_notifiers()
        
        logger.info("通知管理器初始化完成")
    
    def initialize_notifiers(self):
        """初始化所有通知器"""
        notification_config = self.config.get('notification', {})
        
        if notification_config.get('enabled', False):
            # 初始化Telegram通知器
            telegram_config = notification_config.get('telegram', {})
            if telegram_config.get('enabled', False):
                bot_token = telegram_config.get('bot_token', '')
                chat_id = telegram_config.get('chat_id', '')
                
                if bot_token and chat_id:
                    self.notifiers['telegram'] = TelegramNotifier(bot_token, chat_id)
                    logger.info("Telegram通知器已初始化")
                else:
                    logger.warning("Telegram配置不完整，跳过初始化")
        
        logger.info(f"已初始化 {len(self.notifiers)} 个通知器")
    
    async def initialize_all(self):
        """初始化所有通知器（异步）"""
        for name, notifier in self.notifiers.items():
            if hasattr(notifier, 'initialize'):
                await notifier.initialize()
    
    def should_send_notification(self, currency: str, notification_type: str = 'analysis') -> bool:
        """检查是否应该发送通知（冷却时间控制）"""
        key = f"{currency}_{notification_type}"
        cooldown = self.config.get('notification', {}).get('cooldown', 300)
        
        current_time = datetime.now().timestamp()
        last_sent = self.cooldown_tracker.get(key, 0)
        
        if current_time - last_sent >= cooldown:
            self.cooldown_tracker[key] = current_time
            return True
        else:
            remaining = cooldown - (current_time - last_sent)
            logger.debug(f"{currency} {notification_type}通知在冷却中，剩余{remaining:.0f}秒")
            return False
    
    async def send_notification(self, notification_type: str, **kwargs) -> Dict[str, bool]:
        """发送通知"""
        results = {}
        
        for name, notifier in self.notifiers.items():
            try:
                method_name = f"send_{notification_type}"
                if hasattr(notifier, method_name):
                    method = getattr(notifier, method_name)
                    success = await method(**kwargs)
                    results[name] = success
                else:
                    logger.warning(f"通知器 {name} 不支持 {notification_type} 通知类型")
                    results[name] = False
            except Exception as e:
                logger.error(f"发送 {notification_type} 通知失败 ({name}): {e}")
                results[name] = False
        
        return results
    
    async def send_price_alert(self, currency: str, price_data: Dict[str, Any]) -> Dict[str, bool]:
        """发送价格警报"""
        if not self.should_send_notification(currency, 'price_alert'):
            return {'skipped': True}
        
        return await self.send_notification('price_alert', currency=currency, price_data=price_data)
    
    async def send_analysis_report(self, currency: str, analysis: Dict[str, Any]) -> Dict[str, bool]:
        """发送分析报告"""
        if not self.should_send_notification(currency, 'analysis_report'):
            return {'skipped': True}
        
        return await self.send_notification('analysis_report', currency=currency, analysis=analysis)
    
    async def send_error_alert(self, error: str, context: str = "") -> Dict[str, bool]:
        """发送错误警报"""
        return await self.send_notification('error_alert', error=error, context=context)
    
    async def test_all_connections(self) -> Dict[str, bool]:
        """测试所有通知器连接"""
        results = {}
        
        for name, notifier in self.notifiers.items():
            try:
                if hasattr(notifier, 'test_connection'):
                    success = await notifier.test_connection()
                    results[name] = success
                else:
                    results[name] = False
            except Exception as e:
                logger.error(f"测试 {name} 连接失败: {e}")
                results[name] = False
        
        return results
    
    def shutdown(self):
        """关闭所有通知器"""
        for name, notifier in self.notifiers.items():
            try:
                if hasattr(notifier, 'shutdown'):
                    notifier.shutdown()
            except Exception as e:
                logger.error(f"关闭 {name} 通知器时出错: {e}")
        
        logger.info("所有通知器已关闭")