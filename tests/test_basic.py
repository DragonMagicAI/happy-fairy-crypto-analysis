#!/usr/bin/env python3
"""
快乐魔仙数字货币分析技能 - 基础测试
"""

import unittest
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.loader import ConfigLoader
from src.api.coingecko import CoinGeckoClient
from src.analysis.indicators import TechnicalIndicators

class TestConfigLoader(unittest.TestCase):
    """配置加载器测试"""
    
    def test_default_config(self):
        """测试默认配置"""
        loader = ConfigLoader()
        config = loader.load()
        
        self.assertIsInstance(config, dict)
        self.assertIn('api', config)
        self.assertIn('currencies', config)
        self.assertIn('analysis', config)
        self.assertIn('notification', config)
        
        # 检查币种配置
        currencies = config['currencies']
        self.assertIsInstance(currencies, list)
        self.assertGreaterEqual(len(currencies), 2)
        
        # 检查BTC配置
        btc_config = loader.get_currency_config('BTC')
        self.assertIsNotNone(btc_config)
        self.assertEqual(btc_config['symbol'], 'BTC')
        self.assertEqual(btc_config['coin_id'], 'bitcoin')
        
        # 检查ETH配置
        eth_config = loader.get_currency_config('ETH')
        self.assertIsNotNone(eth_config)
        self.assertEqual(eth_config['symbol'], 'ETH')
        self.assertEqual(eth_config['coin_id'], 'ethereum')

class TestCoinGeckoClient(unittest.TestCase):
    """CoinGecko客户端测试"""
    
    def setUp(self):
        """测试前准备"""
        self.client = CoinGeckoClient()
    
    def test_api_status(self):
        """测试API状态检查"""
        status = self.client.check_api_status()
        self.assertIsInstance(status, dict)
        self.assertIn('status', status)
        
        # API应该在线或至少能连接
        self.assertIn(status['status'], ['online', 'error', 'offline'])
    
    def test_get_price_structure(self):
        """测试获取价格数据结构"""
        # 注意：这个测试不实际调用API，只检查方法存在
        self.assertTrue(hasattr(self.client, 'get_price'))
        self.assertTrue(hasattr(self.client, 'get_coin_info'))
        self.assertTrue(hasattr(self.client, 'get_market_data'))

class TestTechnicalIndicators(unittest.TestCase):
    """技术指标测试"""
    
    def setUp(self):
        """测试前准备"""
        self.indicators = TechnicalIndicators()
    
    def test_calculate_ma(self):
        """测试移动平均线计算"""
        prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        ma5 = self.indicators.calculate_ma(prices, 5)
        
        self.assertIsInstance(ma5, list)
        self.assertEqual(len(ma5), len(prices))
        
        # 检查前4个值应该是0（数据不足）
        for i in range(4):
            self.assertEqual(ma5[i], 0.0)
        
        # 第5个值应该是前5个价格的平均
        self.assertAlmostEqual(ma5[4], sum(prices[:5]) / 5)
    
    def test_calculate_macd_structure(self):
        """测试MACD计算结构"""
        prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        macd_result = self.indicators.calculate_macd(prices, 6, 7, 6)
        
        self.assertIsInstance(macd_result, dict)
        self.assertIn('macd', macd_result)
        self.assertIn('signal', macd_result)
        self.assertIn('histogram', macd_result)
        
        # 检查所有列表长度一致
        self.assertEqual(len(macd_result['macd']), len(prices))
        self.assertEqual(len(macd_result['signal']), len(prices))
        self.assertEqual(len(macd_result['histogram']), len(prices))
    
    def test_generate_signals(self):
        """测试信号生成"""
        indicators = {
            'MA5': [100, 101, 102],
            'MA48': [99, 100, 101],
            'MA180': [98, 99, 100]
        }
        
        signals = self.indicators.generate_signals(indicators, 105)
        
        self.assertIsInstance(signals, dict)
        self.assertIn('technical_signal', signals)
        self.assertIn('signal_strength', signals)
        self.assertIn('reason', signals)
        self.assertIn('recommendation', signals)
        
        # 检查信号类型
        valid_signals = ['强烈买入', '买入', '观望', '卖出', '强烈卖出', '错误']
        self.assertIn(signals['technical_signal'], valid_signals)
        
        # 检查信号强度范围
        self.assertGreaterEqual(signals['signal_strength'], 0.0)
        self.assertLessEqual(signals['signal_strength'], 1.0)

if __name__ == '__main__':
    unittest.main()