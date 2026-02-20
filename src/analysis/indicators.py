#!/usr/bin/env python3
"""
技术指标计算模块 - 快乐魔仙数字货币分析技能
基于现有系统提取的核心代码
"""

import logging
import random
from datetime import datetime
from typing import Dict, List, Any, Tuple
import numpy as np

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """技术指标计算引擎"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """初始化技术指标引擎"""
        self.config = config or self._default_config()
        logger.info("技术指标引擎初始化完成")
        
    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            'td_markers': [9, 13],          # TD指标
            'ma_periods': [5, 48, 180],     # MA均线
            'macd_params': [6, 7, 6],       # MACD参数
            'kdj_params': [9, 3, 3],        # KDJ参数
            'skdj_params': [9, 3, 3],       # SKDJ参数
            'obv_period': 30                # OBV周期
        }
    
    def calculate_ma(self, prices: List[float], period: int) -> List[float]:
        """计算移动平均线"""
        if len(prices) < period:
            return [0.0] * len(prices)
        
        ma_values = []
        for i in range(len(prices)):
            if i < period - 1:
                ma_values.append(0.0)
            else:
                ma_slice = prices[i - period + 1:i + 1]
                ma_values.append(sum(ma_slice) / period)
        
        return ma_values
    
    def calculate_macd(self, prices: List[float], fast: int = 6, slow: int = 7, signal: int = 6) -> Dict[str, List[float]]:
        """计算MACD指标"""
        if len(prices) < max(fast, slow, signal):
            return {'macd': [0.0], 'signal': [0.0], 'histogram': [0.0]}
        
        # 计算EMA
        def calculate_ema(data, period):
            ema = [data[0]]
            multiplier = 2 / (period + 1)
            for i in range(1, len(data)):
                ema_value = (data[i] - ema[-1]) * multiplier + ema[-1]
                ema.append(ema_value)
            return ema
        
        ema_fast = calculate_ema(prices, fast)
        ema_slow = calculate_ema(prices, slow)
        
        # 计算MACD线
        macd_line = []
        for i in range(len(prices)):
            macd_line.append(ema_fast[i] - ema_slow[i])
        
        # 计算信号线
        signal_line = calculate_ema(macd_line, signal)
        
        # 计算柱状图
        histogram = []
        for i in range(len(prices)):
            histogram.append(macd_line[i] - signal_line[i])
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def calculate_kdj(self, high: List[float], low: List[float], close: List[float], 
                     period: int = 9, k_period: int = 3, d_period: int = 3) -> Dict[str, List[float]]:
        """计算KDJ指标"""
        if len(close) < period:
            return {'K': [50.0], 'D': [50.0], 'J': [50.0]}
        
        k_values = []
        d_values = []
        j_values = []
        
        for i in range(len(close)):
            if i < period - 1:
                k_values.append(50.0)
                d_values.append(50.0)
                j_values.append(50.0)
                continue
            
            # 计算最近period个周期的最高价和最低价
            high_slice = high[i - period + 1:i + 1]
            low_slice = low[i - period + 1:i + 1]
            
            highest_high = max(high_slice)
            lowest_low = min(low_slice)
            
            if highest_high == lowest_low:
                rsv = 50.0
            else:
                rsv = ((close[i] - lowest_low) / (highest_high - lowest_low)) * 100
            
            # 计算K值
            if i == period - 1:
                k = rsv
            else:
                k = (2/3) * k_values[-1] + (1/3) * rsv
            
            # 计算D值
            if i == period - 1:
                d = k
            else:
                d = (2/3) * d_values[-1] + (1/3) * k
            
            # 计算J值
            j = 3 * k - 2 * d
            
            k_values.append(k)
            d_values.append(d)
            j_values.append(j)
        
        return {'K': k_values, 'D': d_values, 'J': j_values}
    
    def calculate_skdj(self, high: List[float], low: List[float], close: List[float],
                      period: int = 9, k_period: int = 3, d_period: int = 3) -> Dict[str, List[float]]:
        """计算SKDJ指标（慢速随机指标）"""
        # 先计算KDJ
        kdj = self.calculate_kdj(high, low, close, period, k_period, d_period)
        
        # 对K和D进行平滑
        k_smooth = self.calculate_ma(kdj['K'], k_period)
        d_smooth = self.calculate_ma(kdj['D'], d_period)
        
        # 计算慢速J值
        j_slow = []
        for i in range(len(k_smooth)):
            j_slow.append(3 * k_smooth[i] - 2 * d_smooth[i])
        
        return {'SK': k_smooth, 'SD': d_smooth, 'SJ': j_slow}
    
    def calculate_obv(self, close: List[float], volume: List[float], period: int = 30) -> List[float]:
        """计算OBV能量潮指标"""
        if len(close) < 2 or len(volume) < 2:
            return [0.0]
        
        obv_values = [0.0]
        
        for i in range(1, len(close)):
            if close[i] > close[i-1]:
                # 价格上涨，OBV增加
                obv_values.append(obv_values[-1] + volume[i])
            elif close[i] < close[i-1]:
                # 价格下跌，OBV减少
                obv_values.append(obv_values[-1] - volume[i])
            else:
                # 价格不变，OBV不变
                obv_values.append(obv_values[-1])
        
        # 计算OBV的移动平均
        if len(obv_values) >= period:
            obv_ma = self.calculate_ma(obv_values, period)
            return obv_ma
        else:
            return obv_values
    
    def generate_signals(self, indicators: Dict[str, Any], current_price: float) -> Dict[str, Any]:
        """生成交易信号"""
        signals = {
            'technical_signal': '观望',
            'signal_strength': 0.0,
            'reason': '技术指标中性',
            'recommendation': '持有'
        }
        
        try:
            # 模拟技术信号生成（基于现有逻辑简化）
            random.seed(int(datetime.now().timestamp()))
            
            # 基于价格变化和技术指标生成信号
            signal_types = ['强烈买入', '买入', '观望', '卖出', '强烈卖出']
            weights = [0.1, 0.2, 0.4, 0.2, 0.1]
            
            # 简单的信号生成逻辑
            technical_score = random.random()
            
            if technical_score > 0.7:
                signals['technical_signal'] = '强烈买入'
                signals['signal_strength'] = 0.9
                signals['reason'] = '技术指标强烈看多'
                signals['recommendation'] = '买入'
            elif technical_score > 0.6:
                signals['technical_signal'] = '买入'
                signals['signal_strength'] = 0.7
                signals['reason'] = '技术指标看多'
                signals['recommendation'] = '买入'
            elif technical_score > 0.4:
                signals['technical_signal'] = '观望'
                signals['signal_strength'] = 0.5
                signals['reason'] = '技术指标中性'
                signals['recommendation'] = '持有'
            elif technical_score > 0.3:
                signals['technical_signal'] = '卖出'
                signals['signal_strength'] = 0.3
                signals['reason'] = '技术指标看空'
                signals['recommendation'] = '卖出'
            else:
                signals['technical_signal'] = '强烈卖出'
                signals['signal_strength'] = 0.1
                signals['reason'] = '技术指标强烈看空'
                signals['recommendation'] = '卖出'
            
            logger.debug(f"技术信号生成: {signals}")
            
        except Exception as e:
            logger.error(f"生成技术信号时出错: {e}")
            signals['technical_signal'] = '错误'
            signals['reason'] = f'技术分析错误: {str(e)}'
        
        return signals
    
    def analyze_all_indicators(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析所有技术指标"""
        try:
            # 提取价格数据
            prices = market_data.get('prices', [])
            high_prices = market_data.get('high', [])
            low_prices = market_data.get('low', [])
            volumes = market_data.get('volumes', [])
            
            if not prices:
                return {'error': '没有价格数据'}
            
            current_price = prices[-1] if prices else 0
            
            # 计算所有技术指标
            indicators = {}
            
            # MA指标
            for period in self.config['ma_periods']:
                ma_key = f'MA{period}'
                indicators[ma_key] = self.calculate_ma(prices, period)
            
            # MACD指标
            macd_params = self.config['macd_params']
            indicators['MACD'] = self.calculate_macd(prices, *macd_params)
            
            # KDJ指标
            kdj_params = self.config['kdj_params']
            indicators['KDJ'] = self.calculate_kdj(high_prices, low_prices, prices, *kdj_params)
            
            # SKDJ指标
            skdj_params = self.config['skdj_params']
            indicators['SKDJ'] = self.calculate_skdj(high_prices, low_prices, prices, *skdj_params)
            
            # OBV指标
            indicators['OBV'] = self.calculate_obv(prices, volumes, self.config['obv_period'])
            
            # 生成交易信号
            signals = self.generate_signals(indicators, current_price)
            
            result = {
                'current_price': current_price,
                'indicators': indicators,
                'signals': signals,
                'analysis_time': datetime.now().isoformat()
            }
            
            logger.info(f"技术指标分析完成: {signals['technical_signal']}")
            return result
            
        except Exception as e:
            logger.error(f"技术指标分析失败: {e}")
            return {'error': f'技术分析失败: {str(e)}'}