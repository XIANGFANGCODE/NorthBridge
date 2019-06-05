import sys
sys.path.append("..")
from common.scaffold import *

class Transaction:
    """
    交易类，为实际与测试模式或者交易所交易结果
    """
    def __init__(self, exchange, id_from_exchange, object, object_type, object_action,
                 amount_of_object, amount_of_basic_currency, datetime, deal_amount_of_object,
                 deal_amount_of_basic_currency, fee):
        """
        :param id: transaction id
        :param id_from_exchange: 交易所返回的交易id
        :param exchange: 交易所
        :param object: 标的
        :param object_type: 标的类型 spot 或 futures
        :param object_action: 交易方向 buy 或者 sell
        :param amount_of_object: 买卖标的数量
        :param amount_of_basic_currency: 折合基准货币金额，加密货币为ustd，股票期货期权为CNY
        :param datetime: 订单时间
        :param deal_amount_of_object: 成交数量
        :param deal_amount_of_basic_currency: 成交金额
        :param fee: 手续费
        """
        self.id = get_id('transaction')
        self.exchange = exchange
        self.id_from_exchange = id_from_exchange
        self.object = object
        self.object_type = object_type
        self.object_action = object_action
        self.amount_of_object = amount_of_object
        self.amount_of_basic_currency = amount_of_basic_currency
        self.datetime = datetime
        self.deal_amount_of_object = deal_amount_of_object
        self.deal_amount_of_basic_currency = deal_amount_of_basic_currency
        self.fee = fee

    def desc(self):
        print('id is : {}, exchange is : {}, id_from_exchange is : {}, object is : {}, object_type is : {},'
              'object_action is : {}, amount_of_object is : {}, amount_of_basic_currency is : {},'
              'datetime is : {}, deal_amount_of_object is : {}, deal_amount_of_basic_currency is : {},'
              'fee is : {}'.format(
            self.id,
            self.exchange,
            self.id_from_exchange,
            self.object,
            self.object_type,
            self.object_action,
            self.amount_of_object,
            self.amount_of_basic_currency,
            self.datetime,
            self.deal_amount_of_object,
            self.deal_amount_of_basic_currency,
            self.fee
        ))


class SpotTransaction(Transaction):
    """
    现货交易
    """
    def __init__(self,exchange, id_from_exchange, object, object_type, object_action,
                 amount_of_object, amount_of_basic_currency, datetime, deal_amount_of_object,
                 deal_amount_of_basic_currency, fee, price, deal_price):
        """

        :param price: 报价
        :param deal_price: 成交均价
        """
        Transaction.__init__(self, exchange, id_from_exchange, object, object_type, object_action,
                 amount_of_object, amount_of_basic_currency, datetime, deal_amount_of_object,
                 deal_amount_of_basic_currency, fee)
        self.price = price
        self.deal_price = deal_price

    def desc(self):
        print('id is : {}, exchange is : {}, id_from_exchange is : {}, object is : {}, object_type is : {},'
              'object_action is : {}, amount_of_object is : {}, amount_of_basic_currency is : {},'
              'datetime is : {}, deal_amount_of_object is : {}, deal_amount_of_basic_currency is : {},'
              'fee is : {}, price is : {},  deal_price is : {}'.format(
            self.id,
            self.exchange,
            self.id_from_exchange,
            self.object,
            self.object_type,
            self.object_action,
            self.amount_of_object,
            self.amount_of_basic_currency,
            self.datetime,
            self.deal_amount_of_object,
            self.deal_amount_of_basic_currency,
            self.fee,
            self.price,
            self.deal_price
        ))

class FuturesTransaction(Transaction):
    """
    期货/合约交易
    """
    def __init__(self, exchange, id_from_exchange, object, object_type, object_action,
                 amount_of_object, amount_of_basic_currency, datetime, deal_amount_of_object,
                 deal_amount_of_basic_currency, fee, futures_action, futures_price,
                 price, deal_price):
        """

        :param futures_action: 合约类型 buy多 sell空
        :param futures_price: 合约买价
        :param price: 交易报价
        :param deal_price: 成交价
        """
        Transaction.__init__(self, exchange, id_from_exchange, object, object_type, object_action,
                 amount_of_object, amount_of_basic_currency, datetime, deal_amount_of_object,
                 deal_amount_of_basic_currency, fee)
        self.futures_action = futures_action
        self.futures_price = futures_price
        self.price = price
        self.deal_price = deal_price

    def desc(self):
        print('id is : {}, exchange is : {}, id_from_exchange is : {}, object is : {}, object_type is : {},'
              'object_action is : {}, amount_of_object is : {}, amount_of_basic_currency is : {},'
              'datetime is : {}, deal_amount_of_object is : {}, deal_amount_of_basic_currency is : {},'
              'fee is : {}, futures_action is : {}, futures_price is : {}, price is : {},  deal_price is : {}'.format(
            self.id,
            self.exchange,
            self.id_from_exchange,
            self.object,
            self.object_type,
            self.object_action,
            self.amount_of_object,
            self.amount_of_basic_currency,
            self.datetime,
            self.deal_amount_of_object,
            self.deal_amount_of_basic_currency,
            self.fee,
            self.futures_action,
            self.futures_price,
            self.price,
            self.deal_price
        ))
