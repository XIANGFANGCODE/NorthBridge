from common.scaffold import *
import pandas as pd
import numpy as np
from os import path
from resources.signal import *

class Alpha:

    def __init__(self, mode='test'):
        self.mode = mode

    def moving_average(self, short_num, long_num, object, exchange):
        """
        移动均线策略，当一个短期均线与长期均线相交，且短期均线之后高于长期均线后
        认为是一个上涨趋势，发出购买信号，否则认为是一个下跌趋势，发出卖出信号
        :param short_num: M日短期均线
        :param long_num: N日长期均线
        :param object: 标的
        :param exchange: 交易所
        :return: 信号数组
        """
        signals = list()
        if self.mode == 'test':
            signals = self.__moving_average_test(short_num, long_num, object, exchange)
        elif self.mode == 'real':
            signals = self.__moving_average_real(short_num, long_num, object, exchange)
        else:
            logging.error('alpha do not have mode ' + self.mode)
        return signals

    def __moving_average_test(self, short_num, long_num, object, exchange):
        """
        移动均线历史回测函数
        :param short: M日短期均线
        :param long: N日长期均线
        :param object: 标的
        :param exchange: 交易所
        :return: 信号数组
        """
        signals = list()
        history_data_source = path.join(path.dirname(path.dirname(path.realpath(__file__))),
                                        'data',
                                        'digital_cash',
                                        '{}_history_from_{}.csv'.format(object, exchange))
        if not path.exists(history_data_source):
            logging.error('File {} is not exist!'.format(history_data_source))
            return signals

        df = pd.read_csv(history_data_source,
                         dtype={
                             'seq' : str,
                             'date' : str,
                             'price' : np.float64,
                             'volume' : np.float64
                         })
        row_num, _ = df.shape
        pre_short_ma = 0.0
        pre_long_ma = 0.0
        for i in range(row_num):
            if i + 1 <= long_num:
                continue
            short_ma = np.mean(df.iloc[i - short_num + 1 : i + 1, TUSHARE_DATA_TYPE['price']])
            long_ma = np.mean(df.iloc[i - long_num + 1 : i + 1, TUSHARE_DATA_TYPE['price']])
            # 上一次的移动均线有值时才能进行比较
            if pre_short_ma > 0 and pre_long_ma > 0:
                if pre_short_ma <= pre_long_ma and short_ma > long_ma:
                    signal = SignalMA(get_id('signal'), object, 'buy',
                                      df.iloc[i, TUSHARE_DATA_TYPE['price']],
                                      df.iloc[i, TUSHARE_DATA_TYPE['date']],
                                      pre_short_ma, pre_long_ma,
                                      short_ma,long_ma)
                    signals.append(signal)
                elif pre_short_ma >= pre_long_ma and short_ma < long_ma:
                    signal = SignalMA(get_id('signal'), object, 'sell',
                                      df.iloc[i, TUSHARE_DATA_TYPE['price']],
                                      df.iloc[i, TUSHARE_DATA_TYPE['date']],
                                      pre_short_ma, pre_long_ma,
                                      short_ma, long_ma)
                    signals.append(signal)
                else:
                    pass
            pre_short_ma = short_ma
            pre_long_ma = long_ma
        return signals

    def __moving_average_real(self, short_num, long_num, object, exchange):
        signals = list()
        return signals
