import sys
sys.path.append("..")
from common.scaffold import *

class Signal:
    """
    信号：指在指定的策略下，根据当前或者历史市场数据，产生可能的交易机会
    """
    def __init__(self, exchange, object, action, price, datetime):
        """
        signal init
        :param id:  信号id，唯一标识信号
        :param exchange:  交易所
        :param object: 交易标的
        :param action: 交易行为买或卖
        :param price: 交易价格
        :param datetime: 信号产生时间
        """
        self.id = get_id('signal')
        self.exchange = exchange
        self.object = object
        self.action = action
        self.price = price
        self.datetime = datetime

    def desc(self):
        print('id : {}, object : {}, action : {}, price : {}, datetime : {}.'.format(
            self.id,
            self.object,
            self.action,
            self.price,
            self.datetime
        ))



#移动均线信号
class SignalMA(Signal):

    def __init__(self, exchange, object, action, price, datetime,
                 pre_short_ma, pre_long_ma, short_ma, long_ma):
        Signal.__init__(self, exchange, object, action, price, datetime)
        self.pre_short_ma = pre_short_ma
        self.pre_long_ma = pre_long_ma
        self.short_ma = short_ma
        self.long_ma = long_ma

    def desc(self):
        print('id : {}, exchange: {}, object : {}, action : {}, price : {}, datetime : {}, '
              'pre_short_ma : {}, pre_long_ma : {} , short_ma : {}, long_ma : {}.'.format(
            self.id,
            self.exchange,
            self.object,
            self.action,
            self.price,
            self.datetime,
            self.pre_short_ma,
            self.pre_long_ma,
            self.short_ma,
            self.long_ma
        ))