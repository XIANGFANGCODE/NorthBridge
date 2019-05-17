import sys
sys.path.append("..")
from common.scaffold import *
import logging


class Order:
    def __init__(self, id, exchange, object, object_type, object_action, amount_of_object,
                 price, amount_of_basic_currency, datetime, futures_action=''):
        """
        订单类，描述如何向交易所下订单
        注意 order不是成交情况
        :param id: order id
        :param exchange: 交易所
        :param object: 标的
        :param object_type: 标的类型 spot 或 futures
        :param object_action: 交易方向 buy 或者 sell
        :param amount_of_object: 买卖标的数量
        :param futures_action: 若标的为合约，标明是空还是多
        :param price: 买卖标的价格
        :param amount_of_basic_currency: 折合基准货币金额，加密货币为ustd，股票期货期权为CNY
        :param datetime: 订单时间
        """
        self.id = get_id('order')
        self.exchange = exchange
        self.object = object
        self.object_type = object_type
        self.object_action = object_action
        self.amount_of_object = amount_of_object
        self.price = price
        self.amount_of_basic_currency = amount_of_basic_currency
        self.datetime = datetime
        self.futures_action = futures_action

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
                basic_currency_in_account = get_value_from_dict(account.spot_account.account, signal.exchange,
                                                                basic_currency)
                if basic_currency_in_account is None or basic_currency_in_account < 1:
                    logging.info('No {} in account of exchange {}.'.format(basic_currency, signal.exchange))
                else:
                    order = Order._buy_spot(account, signal, basic_currency_in_account)
                    if order is not None:
                        orders.append(order)
            elif trade_limit == 'both':
                # 1. 平空头合约
                futures_list = get_value_from_dict(account.futures_account.account, signal.exchange, signal.object)
                if futures_list is None or len(futures_list) == 0:
                    logging.info('No futures {} in account of exchange {}.'.format(signal.object, signal.exchange))
                else:
                    for future in futures_list:
                        action = future.get('action')
                        if action is not None and action == 'sell':
                            order, basic_currency_by_sell = Order._sell_futures(account, signal, future)
                            if order is not None:
                                orders.append(order)
                                # 2. 平仓金额买现货
                                if basic_currency_by_sell is not None and basic_currency_by_sell > 1:
                                    order = Order._buy_spot(account, signal, basic_currency_by_sell)
                                    if order is not None:
                                        orders.append(order)
                # 3. 原有账户余额买现货
                basic_currency = get_basic_currency(signal.object)
                basic_currency_in_account = get_value_from_dict(account.spot_account.account, signal.exchange,
                                                                basic_currency)
                if basic_currency_in_account is None or basic_currency_in_account < 1:
                    logging.info('No {} in account of exchange {}.'.format(basic_currency, signal.exchange))
                else:
                    order = Order._buy_spot(account, signal, basic_currency_in_account)
                    if order is not None:
                        orders.append(order)
            else:
                # 平空头合约
                futures_list = get_value_from_dict(account.futures_account.account, signal.exchange, signal.object)
                if futures_list is None or len(futures_list) == 0:
                    logging.info('No futures {} in account of exchange {}.'.format(signal.object, signal.exchange))
                else:
                    for future in futures_list:
                        action = future.get('action')
                        if action is not None and action == 'sell':
                            order, basic_currency_by_sell = Order._sell_futures(account, signal, future)
                            if order is not None:
                                orders.append(order)

        elif signal.action == 'sell':
            if trade_limit == 'sell':
                # 开空仓合约
                basic_currency = get_basic_currency(signal.object)
                basic_currency_in_account = get_value_from_dict(account.spot_account.account, signal.exchange,
                                                                basic_currency)
                if basic_currency_in_account is None or basic_currency_in_account < 1:
                    logging.info('No {} in account of exchange {}.'.format(basic_currency, signal.exchange))
                else:
                    order = Order._buy_futures(account, signal, basic_currency_in_account)
                    if order is not None:
                        orders.append(order)
            elif trade_limit == 'both':
                # 卖现货
                spot = get_value_from_dict(account.spot_account.account, signal.exchange, signal.object)
                if spot is None or spot <= 0:
                    logging.info('No spot {} in account of exchange {}.'.format(signal.object, signal.exchange))
                else:
                    order, basic_currency_by_sell = Order._sell_spot(account, signal, spot)
                    if order is not None:
                        orders.append(order)
                        if basic_currency_by_sell is not None and basic_currency_by_sell > 1:
                            # 开空仓合约
                            order = Order._buy_futures(account, signal, basic_currency_by_sell)
                            if order is not None:
                                orders.append(order)
                # 开空仓合约
                basic_currency = get_basic_currency(signal.object)
                basic_currency_in_account = get_value_from_dict(account.spot_account.account, signal.exchange,
                                                                basic_currency)
                if basic_currency_in_account is None:
                    logging.info('No {} in account of exchange {}.'.format(basic_currency, signal.exchange))
                else:
                    order = Order._buy_futures(account, signal, basic_currency_in_account)
                    if order is not None:
                        orders.append(order)
            else:
                # 卖现货
                spot = get_value_from_dict(account.spot_account.account, signal.exchange, signal.object)
                if spot is None or spot <= 0:
                    logging.info('No spot {} in account of exchange {}.'.format(signal.object, signal.exchange))
                else:
                    order, basic_currency_by_sell = Order._sell_spot(account, signal, spot)
                    if order is not None:
                        orders.append(order)
        else:
            logging.error('signal has no action: ' + signal.action)
        return orders

    @staticmethod
    def _buy_spot(account, signal, basic_currency_in_account):
        """
        购买现货
        :param account: 账户
        :param signal: 信号
        :return:
        """
        if basic_currency_in_account < 1:
            logging.info('Not sufficient {}.'.format(basic_currency_in_account))
            return None
        amount_of_object = float('%.2f' % (basic_currency_in_account / signal.price))
        amount_of_basic_currency = amount_of_object * signal.price
        order = Order(exchange=signal.exchange,
                      object=signal.object,
                      object_type='spot',
                      object_action='buy',
                      amount_of_object=amount_of_object,
                      price=signal.price,
                      amount_of_basic_currency=amount_of_basic_currency,
                      datetime=signal.datetime)
        return order

    @staticmethod
    def _sell_spot(account, signal, amount_of_spot):
        """
        卖出现货
        :param account: 账户
        :param signal: 信号
        :param amount_of_spot: 现货数量
        :return:
        """
        basic_currency_by_sell = amount_of_spot * signal.price
        order = Order(exchange=signal.exchange,
                      object=signal.object,
                      object_type='spot',
                      object_action='sell',
                      amount_of_object=amount_of_spot,
                      price=signal.price,
                      amount_of_basic_currency=basic_currency_by_sell,
                      datetime=signal.datetime
                      )
        return order, basic_currency_by_sell

    @staticmethod
    def _buy_futures(account, signal, basic_currency_in_account):
        """
        买期货/合约
        :param account: 账号
        :param signal: 信号
        :return:
        """
        if basic_currency_in_account < 1:
            logging.info('Not sufficient {}.'.format(basic_currency_in_account))
            return None
        amount_of_object = float('%.2f' % (basic_currency_in_account / signal.price))
        amount_of_basic_currency = amount_of_object * signal.price
        order = Order(exchange=signal.exchange,
                      object=signal.object,
                      object_type='futures',
                      object_action='buy',
                      amount_of_object=amount_of_object,
                      price=signal.price,
                      amount_of_basic_currency=amount_of_basic_currency,
                      datetime=signal.datetime,
                      futures_action=signal.action)
        return order

    @staticmethod
    def _sell_futures(account, signal, future):
        """
        卖期货/合约
        :param account: 账号
        :param signal: 信号
        :param future: 持有合约情况
        :return:
        """
        if future.get('action') is None or future.get('price') is None or future.get('value') is None or \
                future.get('price') < 0 or future.get('value') <= 0:
            return None, 0
        if future.get('action') == 'sell':
            amount_of_basic_currency = (future.price * future.value) - (signal.price - future.price) * future.value
        else:
            amount_of_basic_currency = (future.price * future.value) + (signal.price - future.price) * future.value
        order = Order(exchange=signal.exchange,
                      object=signal.object,
                      object_type='futures',
                      object_action='sell',
                      amount_of_object=future.get('value'),
                      price=signal.price,
                      amount_of_basic_currency=amount_of_basic_currency,
                      datetime=signal.datetime,
                      futures_action=future.action)
        return order, amount_of_basic_currency

    def desc(self):
        print('id is : {}, exchange is : {}, object is : {}, object_type is : {}, object_action is : {},'
              'amount_of_object is : {}, price is : {}, amount_of_basic_currency is : {},'
              'datetime is : {}, futures_action is : {}'.format(
            self.id,
            self.exchange,
            self.object,
            self.object_type,
            self.object_action,
            self.amount_of_object,
            self.price,
            self.amount_of_basic_currency,
            self.datetime,
            self.futures_action
        ))