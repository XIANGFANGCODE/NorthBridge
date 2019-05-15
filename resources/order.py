from resources.account import Account
from resources.signal import Signal
import sys
sys.path.append("..")
from common.scaffold import *

import logging


class Order:
    def __init__(self, exchange, object, object_type, object_action, amount_of_object, price, amount_of_money, datetime):
        """
        订单类，描述如何向交易所下订单
        注意 order不是成交情况
        :param exchange: 交易所
        :param object: 标的
        :param object_type: 标的类型 spot 或 futures
        :param object_action: 交易方向 buy 或者 sell
        :param amount_of_object: 买入标的数量
        :param price: 买入标的价格
        :param amount_of_money: 折合基准货币金额，加密货币为ustd，股票期货期权为CNY
        :param datetime: 订单时间
        """
        self.exchange = exchange
        self.object = object
        self.object_type = object_type
        self.object_action = object_action
        self.amount_of_object = amount_of_object
        self.price = price
        self.amount_of_money = amount_of_money
        self.datetime = datetime

    def desc(self):
        print('exchange: {}, object: {}, object_type ： {}, object_action: {}, '
              'amount_of_object: {}, price: {}, amount_of_money: {}, datetime: {}'.format(
            self.exchange,
            self.object,
            self.object_type,
            self.object_action,
            self.amount_of_object,
            self.price,
            self.amount_of_money,
            self.datetime
        ))

    @staticmethod
    def create_orders(mode, trade_limit, account, signal, **kw):
        """
        根据账户和信号创建订单
        :param mode: 下单策略
        :param trade_limit: 交易限制（只做多、只做空或者同时都能做）
        :param account: 账户
        :param signal: 信号,order类只关心基类signal的属性，不关心子类的信息
        :param **kw： 根据mode不同，可能需要传入不同的参数
        :return: 订单列表
        """
        # 合法性检查
        orders = list()
        if mode == 'allin':
            orders = Order._create_orders_by_allin(trade_limit, account, signal)
        else:
            logging.error('create_orders has no mode: '.format(mode))

        return orders

    @staticmethod
    def _create_orders_by_allin(trade_limit, account, signal):
        """
        All in 下单
        :param trade_limit: 交易限制（只做多、只做空或者同时都能做）
        :param account: 账户
        :param signal: 信号,order类只关心基类signal的属性，不关心子类的信息
        :param **kw： 根据mode不同，可能需要传入不同的参数
        :return: 订单列表
        """
        orders = list()
        if signal.action == 'buy':
            if trade_limit == 'buy':
                # 买现货
                basic_currency = get_basic_currency(signal.object)
                amount_of_basic_currency = account.spot_account.account[signal.exchange][basic_currency]
                order = Order._buy_spot(account, signal, amount_of_basic_currency)
                if order is not None:
                    orders.append(order)
            elif trade_limit == 'both':
                # 1. 平空头合约
                futures = account.futures_account.account[signal.exchange][signal.object]
                # 2. 买现货

            else:
                # 交易限制为sell，忽略buy信号
                pass
        elif signal.action == 'sell':
            pass
        else:
            logging.error('signal has no action: ' + signal.action)
        return orders

    @staticmethod
    def _buy_spot(account, signal, amount_of_basic_currency):
        """
        购买现货
        :param account: 账户
        :param signal: 信号
        :return:
        """
        if amount_of_basic_currency < 1:
            logging.info('Not sufficient {}.'.format(amount_of_basic_currency))
            return None
        amount_of_object = float('%.2f' % (amount_of_basic_currency / signal.price))
        amount_of_money = amount_of_object * signal.price
        order = Order(exchange=signal.exchange,
                      object=signal.object,
                      object_type='spot',
                      object_action='buy',
                      amount_of_object=amount_of_object,
                      price=signal.price,
                      amount_of_money=amount_of_money,
                      datetime=signal.datetime)
        return order

    @staticmethod
    def _sell_spot(account, signal):
        """
        卖出现货
        :param account: 账户
        :param signal: 信号
        :return:
        """


    @staticmethod
    def _buy_futures(account, signal):
        """
        买期货/合约
        :param account: 账号
        :param signal: 信号
        :return:
        """
        orders = list()
        return orders


    @staticmethod
    def _sell_futures(account, signal):
        """
        买期货/合约
        :param account: 账号
        :param signal: 信号
        :return:
        """
        order = Order(exchange=signal.exchange,
                      object=signal.object,
                      object_type='futures',
                      object_action='sell',
                      amount_of_object=account.futures_account.account[signal.exchange][])
        return order