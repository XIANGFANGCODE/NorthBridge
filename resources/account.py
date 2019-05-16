import logging

class SpotAccount:
    """
    现货账户
    数据模型为一个2级字典
            {
            "tushare" : {
                "btc" : 100,
                "eth" : 200
                }
        }
    """
    def __init__(self):
        self.account = dict()

class FuturesAccount:
    """
    合约/期货账户，类似如下的一个3级字典
            {
            "tushare" : {
                "btc" : [
                    {"action" : "sell",
                    "price" : 1000,
                    "value" : 100}'
                     {"action" : "buy",
                    "price" : 1000,
                    "value" : 100}'
                    ],
            }
        }
    """
    def __init__(self):
        self.account = dict()


class Account:
    """
    资金账户类，用以现实所有的资产
    数据模型为一个3级字典
    结构如下
    注意区分现货和期货
    """
    def __init__(self, mode):
        self.mode = mode
        self.datetime = ""
        self.spot_account = SpotAccount()
        self.futures_account = FuturesAccount()

    def get_account(self, exchange, datetime, object, start_account=100000):
        """
        获取一个测试或真实账户
        :param exchange: 交易所
        :param datetime: 账户快照日期
        :param start_account: 测试账户初始金额，数字货币统一用USTD计算，股票期货股票用CNY计算
        :return: Account类
        """
        self.datetime = datetime
        if self.mode == 'test':
            self.spot_account, _ = self._get_test_account(exchange, object, start_account)
        elif self.mode == 'real':
            self.spot_account, _ = self._get_real_account(exchange)
        else:
            logging.error("account has no mode {}.".format(self.mode))
        return self

    def _get_test_account(self, exchange, object, start_account):
        # 测试账户只有现货基准币种
        self.spot_account.account[exchange] = dict()
        self.spot_account.account[exchange][object] = start_account
        return self.spot_account, self.futures_account

    def _get_real_account(self, exchange):
        return self.spot_account, self.futures_account

    def desc(self):
        print("mode: {}, datetime: {}".format(self.mode, self.datetime))
        print("spot account: ")
        for key in self.spot_account.account:
            print("exchange: " + key)
            for i in self.spot_account.account[key]:
                print("object: {}, value: {}".format(i, self.spot_account.account[key][i]))
        print("futures account: ")
        for key in self.futures_account.account:
            print("exchange: " + key)
            for i in self.futures_account.account[key]:
                print("object: " + i)
                for j in self.futures_account.account[key][i]:
                    print("action: {}, price: {}, value: {}".
                          format(self.futures_account.account[key][i][j]['action'],
                                 self.futures_account.account[key][i][j]['price'],
                                 self.futures_account.account[key][i][j]['value']))