from resources.account import Account
from resources.signal import Signal


class Order:
    def __init__(self, exchange, object, amount_of_object, price, amount_of_money, datetime):
        """
        订单类，描述如何向交易所下订单
        注意order不是成交情况
        :param exchange: 交易所
        :param object: 标的
        :param amount_of_object: 买入标的数量
        :param price: 价格
        :param amount_of_money: 折合基准货币金额，加密货币为ustd，股票期货期权为CNY
        :param datetime: 订单时间
        """
        self.exchange = exchange
        self.object = object
        self.amount_of_object = amount_of_object
        self.price = price
        self.amount_of_money = amount_of_money
        self.datetime = datetime

    def desc(self):
        print('exchange: {}, object: {}, amount_of_object: {}, price: {}, amount_of_money: {}, datetime: {}'.format(
            self.exchange,
            self.object,
            self.amount_of_object,
            self.price,
            self.amount_of_money,
            self.datetime
        ))

    @staticmethod
    def create_orders(mode, trade_limit, account, signal):
        """
        根据账户和信号创建订单
        :param mode: 下单策略
        :param trade_limit: 交易限制（只做多、只做空或者同时都能做）
        :param account: 账户
        :param signal: 信号
        :return: 订单列表
        """
        orders = list()
        order = Order('tushare', 'btc', '1', '5000', '5000', '20190501')
        order2 = Order('tushare', 'btc', '2', '5000', '10000', '20190502')
        orders.append(order)
        orders.append(order2)
        return orders
