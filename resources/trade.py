from resources.transaction import *
import sys
sys.path.append("..")
from common.scaffold import *
import logging

class Trade:
    """
    Trade类为与测试/交易所交易交互的类
    """
    def __init__(self, mode='test'):
        """

        :param mode: 模式
        """
        self.mode = mode            #模式
        self.id = get_id('trade')   #trade id
        self.order_id = 0           #订单id
        self.transaction_id = 0     #交易id

    def trade(self, order, account, **kwargs):
        """
        交易
        :param order: 订单
        :param account: 账户
        :return: transaction, account
        """
        if self.mode == 'test':
            if kwargs is not None:
                fee = kwargs.get('fee', 0)
                transaction, account =  self._test_trade(order, account, fee)
                self.transaction_id = transaction.id
                return transaction, account
            else:
                logging.error('_test_trade do not have fee!')
                return None, account
        elif self.mode == 'real':
            return self._real_trade(order, account)
        else:
            logging.error('trade do not have mode ' + self.mode)
            return None, account

    def _test_trade(self, order, account, fee):
        """

        :param order: 订单
        :param fee: 手续费率,类似0.02
        :return: transaction
        """
        self.order_id = order.id
        if order.object_type == 'spot':
            transaction = SpotTransaction(
                exchange=order.exchange,
                id_from_exchange=order.id,
                object=order.object,
                object_type=order.object_type,
                object_action=order.object_action,
                amount_of_object=order.amount_of_object,
                amount_of_basic_currency=order.amount_of_basic_currency,
                datetime=order.datetime,
                deal_amount_of_object=float_mul((1 - fee), order.amount_of_object),
                deal_amount_of_basic_currency=float_mul((1 - fee), order.amount_of_basic_currency),
                fee=fee * order.amount_of_basic_currency,
                price=order.price,
                deal_price=order.price
            )
            # 修改account信息
            basic_currency = get_basic_currency(transaction.object)
            if transaction.object_action == 'buy':    # buy spot
                account.spot_account.account[transaction.exchange][basic_currency]['value'] -= \
                    transaction.amount_of_basic_currency
                if get_value_from_dict(account.spot_account.account, transaction.exchange, transaction.object) is None:
                    account.spot_account.account[transaction.exchange][transaction.object] = dict({
                        'price' : transaction.deal_price,
                        'value' : transaction.deal_amount_of_object
                    })
                else:
                    account.spot_account.account[transaction.exchange][transaction.object]['value'] += \
                        transaction.deal_amount_of_object
                    account.spot_account.account[transaction.exchange][transaction.object]['price'] = \
                        transaction.deal_price
            else:   #sell spot
                account.spot_account.account[transaction.exchange][transaction.object]['value'] -= \
                    transaction.amount_of_object
                if get_value_from_dict(account.spot_account.account, transaction.exchange, basic_currency) is None:
                    account.spot_account.account[transaction.exchange][basic_currency] = dict({
                        'price' : BASIC_CURRENCY_UNIT,
                        'value' : transaction.deal_amount_of_basic_currency
                    })
                else:
                    account.spot_account.account[transaction.exchange][basic_currency]['value'] += \
                        transaction.deal_amount_of_basic_currency
            return transaction, account
        elif order.object_type == 'futures':
            transaction = FuturesTransaction(
                exchange=order.exchange,
                id_from_exchange=order.id,
                object=order.object,
                object_type=order.object_type,
                object_action=order.object_action,
                amount_of_object=order.amount_of_object,
                amount_of_basic_currency=order.amount_of_basic_currency,
                datetime=order.datetime,
                deal_amount_of_object=float_mul((1 - fee), order.amount_of_object),
                deal_amount_of_basic_currency=float_mul((1 - fee), order.amount_of_basic_currency),
                fee=fee * order.amount_of_basic_currency,
                futures_action=order.futures_action,
                futures_price=order.futures_price,
                price=order.price,
                deal_price=order.price
            )
            basic_currency = get_basic_currency(transaction.object)
            if transaction.object_action == 'buy':  # buy futures
                account.spot_account.account[transaction.exchange][basic_currency]['value'] -= \
                    transaction.amount_of_basic_currency
                if get_value_from_dict(account.futures_account.account, transaction.exchange, transaction.object) is None:
                    if get_value_from_dict(account.futures_account.account, transaction.exchange) is None:
                        account.futures_account.account[transaction.exchange] = dict()
                    account.futures_account.account[transaction.exchange][transaction.object] = list()
                    account.futures_account.account[transaction.exchange][transaction.object].append(
                        dict({'action': transaction.futures_action,
                                'price': transaction.deal_price,
                                'value': transaction.deal_amount_of_object}))
                else:
                    future_list = account.futures_account.account[transaction.exchange][transaction.object]
                    j = 0
                    for i in range(len(future_list)):
                        future = future_list[i]
                        if future['action'] == transaction.futures_action and future['price'] == transaction.deal_price:
                            future['value'] = future['value'] + transaction.deal_amount_of_object
                            future_list[i] = future
                            j = 1
                            break
                    if j == 0:
                        account.futures_account.account[transaction.exchange][transaction.object].append(
                            dict({'action': transaction.futures_action,
                                  'price': transaction.deal_price,
                                  'value': transaction.deal_amount_of_object}))
            else:  # sell futures
                future_list = account.futures_account.account[transaction.exchange][transaction.object]
                j = 0
                for i in range(len(future_list)):
                    future = future_list[i]
                    if future['action'] == transaction.futures_action and future['price'] == transaction.futures_price:
                        future['value'] = future['value'] - transaction.amount_of_object
                        future_list[i] = future
                        j = 1
                        break
                if j == 0:
                   logging.error("No sufficient futures : {}, of exchange: {}".format(transaction.exchange,
                                                                                     transaction.object))
                else:
                    if get_value_from_dict(account.spot_account.account, transaction.exchange, basic_currency) is None:
                        account.spot_account.account[transaction.exchange][basic_currency] = dict({
                            'price': BASIC_CURRENCY_UNIT,
                            'value': transaction.deal_amount_of_basic_currency
                        })
                    else:
                        account.spot_account.account[transaction.exchange][basic_currency]['value'] += \
                            transaction.deal_amount_of_basic_currency

            account.datetime = transaction.datetime
            return transaction, account
        else:
            logging.error('order do not have object_type: {}'.format(order.object_type))
            return None, account

    def _real_trade(self, order, account):
        return None, account

    def desc(self):
        print('mode is : {}, id is : {}, order id is : {}, transaction id is : {}'.format(
            self.mode,
            self.id,
            self.order_id,
            self.transaction_id
        ))