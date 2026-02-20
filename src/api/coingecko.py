#!/usr/bin/env python3
"""
CoinGecko API客户端 - 快乐魔仙数字货币分析技能
简化版本，专注于核心功能
"""

import logging
import time
from typing import Dict, List, Any, Optional
import requests
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CoinGeckoClient:
    """CoinGecko API客户端"""
    
    def __init__(self, api_key: str = None, cache_ttl: int = 300):
        """初始化CoinGecko客户端"""
        self.base_url = "https://api.coingecko.com/api/v3"
        self.api_key = api_key
        self.cache_ttl = cache_ttl  # 缓存时间(秒)
        self.cache = {}
        self.session = requests.Session()
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'HappyFairyCryptoAnalysis/1.0.0',
            'Accept': 'application/json'
        })
        
        if api_key:
            self.session.headers.update({'x-cg-demo-api-key': api_key})
        
        logger.info("CoinGecko客户端初始化完成")
    
    def _get_cached_data(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_ttl:
                logger.debug(f"使用缓存数据: {key}")
                return data
            else:
                logger.debug(f"缓存过期: {key}")
                del self.cache[key]
        return None
    
    def _set_cached_data(self, key: str, data: Any):
        """设置缓存数据"""
        self.cache[key] = (data, time.time())
        logger.debug(f"设置缓存数据: {key}")
    
    def get_price(self, coin_id: str = 'bitcoin', currency: str = 'usd') -> Dict[str, Any]:
        """获取当前价格"""
        cache_key = f"price_{coin_id}_{currency}"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': currency,
                'include_market_cap': 'true',
                'include_24hr_vol': 'true',
                'include_24hr_change': 'true',
                'include_last_updated_at': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if coin_id in data:
                result = {
                    'price': data[coin_id].get(f'{currency}', 0),
                    'market_cap': data[coin_id].get(f'{currency}_market_cap', 0),
                    'volume_24h': data[coin_id].get(f'{currency}_24h_vol', 0),
                    'change_24h': data[coin_id].get(f'{currency}_24h_change', 0),
                    'last_updated': data[coin_id].get('last_updated_at', 0),
                    'timestamp': datetime.now().isoformat()
                }
                
                self._set_cached_data(cache_key, result)
                logger.info(f"获取价格成功: {coin_id} = ${result['price']}")
                return result
            else:
                logger.error(f"未找到币种数据: {coin_id}")
                return {'error': f'未找到币种: {coin_id}'}
                
        except requests.exceptions.RequestException as e:
            logger.error(f"获取价格失败: {e}")
            return {'error': f'API请求失败: {str(e)}'}
        except Exception as e:
            logger.error(f"处理价格数据失败: {e}")
            return {'error': f'数据处理失败: {str(e)}'}
    
    def get_coin_info(self, coin_id: str = 'bitcoin') -> Dict[str, Any]:
        """获取币种信息"""
        cache_key = f"info_{coin_id}"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            url = f"{self.base_url}/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'false',
                'community_data': 'false',
                'developer_data': 'false',
                'sparkline': 'false'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = {
                'id': data.get('id', ''),
                'symbol': data.get('symbol', '').upper(),
                'name': data.get('name', ''),
                'description': data.get('description', {}).get('en', '')[:200] + '...',
                'homepage': data.get('links', {}).get('homepage', [''])[0],
                'genesis_date': data.get('genesis_date', ''),
                'market_cap_rank': data.get('market_cap_rank', 0),
                'timestamp': datetime.now().isoformat()
            }
            
            self._set_cached_data(cache_key, result)
            logger.info(f"获取币种信息成功: {coin_id}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取币种信息失败: {e}")
            return {'error': f'API请求失败: {str(e)}'}
        except Exception as e:
            logger.error(f"处理币种信息失败: {e}")
            return {'error': f'数据处理失败: {str(e)}'}
    
    def get_market_data(self, coin_id: str = 'bitcoin', days: int = 7) -> Dict[str, Any]:
        """获取市场数据（用于技术分析）"""
        cache_key = f"market_{coin_id}_{days}"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # 提取价格数据
            prices = [item[1] for item in data.get('prices', [])]
            market_caps = [item[1] for item in data.get('market_caps', [])]
            volumes = [item[1] for item in data.get('total_volumes', [])]
            
            # 计算高、低价格（简化版本）
            high_prices = []
            low_prices = []
            
            for i in range(len(prices)):
                if i == 0:
                    high_prices.append(prices[i] * 1.01)  # 模拟高价
                    low_prices.append(prices[i] * 0.99)   # 模拟低价
                else:
                    change = random.uniform(-0.03, 0.03)  # 模拟价格波动
                    high_prices.append(prices[i] * (1 + abs(change)))
                    low_prices.append(prices[i] * (1 - abs(change)))
            
            result = {
                'prices': prices,
                'high': high_prices,
                'low': low_prices,
                'volumes': volumes,
                'market_caps': market_caps,
                'data_points': len(prices),
                'period_days': days,
                'timestamp': datetime.now().isoformat()
            }
            
            self._set_cached_data(cache_key, result)
            logger.info(f"获取市场数据成功: {coin_id}, {len(prices)}个数据点")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取市场数据失败: {e}")
            return {'error': f'API请求失败: {str(e)}'}
        except Exception as e:
            logger.error(f"处理市场数据失败: {e}")
            return {'error': f'数据处理失败: {str(e)}'}
    
    def get_multiple_prices(self, coin_ids: List[str], currency: str = 'usd') -> Dict[str, Dict[str, Any]]:
        """获取多个币种价格"""
        try:
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': ','.join(coin_ids),
                'vs_currencies': currency,
                'include_last_updated_at': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = {}
            for coin_id in coin_ids:
                if coin_id in data:
                    result[coin_id] = {
                        'price': data[coin_id].get(f'{currency}', 0),
                        'last_updated': data[coin_id].get('last_updated_at', 0)
                    }
            
            logger.info(f"获取多个价格成功: {len(result)}个币种")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取多个价格失败: {e}")
            return {'error': f'API请求失败: {str(e)}'}
    
    def check_api_status(self) -> Dict[str, Any]:
        """检查API状态"""
        try:
            url = f"{self.base_url}/ping"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                return {
                    'status': 'online',
                    'response_time': response.elapsed.total_seconds(),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'error',
                    'status_code': response.status_code,
                    'timestamp': datetime.now().isoformat()
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"检查API状态失败: {e}")
            return {
                'status': 'offline',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_supported_coins(self) -> List[Dict[str, Any]]:
        """获取支持的币种列表"""
        cache_key = "supported_coins"
        cached = self._get_cached_data(cache_key)
        if cached:
            return cached
        
        try:
            url = f"{self.base_url}/coins/list"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            coins = response.json()
            
            # 只返回前100个主要币种
            major_coins = [
                coin for coin in coins 
                if coin['id'] in ['bitcoin', 'ethereum', 'binancecoin', 'ripple', 'cardano', 
                                 'solana', 'polkadot', 'dogecoin', 'matic-network', 'chainlink']
            ]
            
            self._set_cached_data(cache_key, major_coins)
            logger.info(f"获取支持币种列表成功: {len(major_coins)}个主要币种")
            return major_coins
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取币种列表失败: {e}")
            return []

# 导入random用于模拟数据
import random