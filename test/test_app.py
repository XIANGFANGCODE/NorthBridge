import sys
from requests import put, get

"""
parser.add_argument('action', required=True, help="Tell me what should i do?") #行为
parser.add_argument('alpha') #策略
parser.add_argument('risk') #风险
parser.add_argument('cost') #成本
parser.add_argument('order') #订单
parser.add_argument('execute') #执行
parser.add_argument('object') #标的
parser.add_argument('exchange') #交易所
"""

ret = put('http://127.0.0.1:5000/', data={'action': 'do_history_transaction',
                                         'alpha' : 'moving_average',
                                         'order' : 'allin',
                                         'object' : 'btc',
                                         'exchange' : 'tushare'
                                          })
print(ret.json())

