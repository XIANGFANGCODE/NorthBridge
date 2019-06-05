import logging

class SpotAccount:
    """
    现货账户
    数据模型为一个2级字典
            {
            "tushare" : {
                "btc" : {
                    "price": 10,  #为方便计算收益率，存入此值
                    "value" : 100
                    },
                "ustd" : {
                    "price": 1,
                    "value" : 100
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
        self.ustd_unit = 1

    def get_account(self, exchange, datetime, *args):
        """
        获取一个测试或真实账户
        :param exchange: 交易所
        :param datetime: 账户快照日期
        :param *args:
        test模式 args[0] 基准货币类型，数字货币统一用USTD计算，股票期货股票用CNY计算
                args[1] 为测试账户初始金额
        :return: Account类
        """
        self.datetime = datetime
        if self.mode == 'test':
            self.spot_account, self.futures_account = self._get_test_account(exchange, args[0], args[1])
        elif self.mode == 'real':
            self.spot_account, self.futures_account = self._get_real_account(exchange)
        else:
            logging.error("account has no mode {}.".format(self.mode))
        return self

    def _get_test_account(self, exchange, object, start_account):
        # 测试账户只有现货基准币种
        self.spot_account.account[exchange] = dict()
        self.spot_account.account[exchange][object] = dict()
        self.spot_account.account[exchange][object]['price'] = self.ustd_unit
        self.spot_account.account[exchange][object]['value'] = start_account
        return self.spot_account, self.futures_account

    def _get_real_account(self, exchange):
        return self.spot_account, self.futures_account

    def desc(self):
        print("mode: {}, datetime: {}".format(self.mode, self.datetime))
        print("spot account: ")
        for key in self.spot_account.account:
            print("exchange: " + key)
            for i in self.spot_account.account[key]:
                print("object: {} ".format(i))
                print("price: {}, value: {}".format(self.spot_account.account[key][i]['price'],
                                                    self.spot_account.account[key][i]['value']))
        print("futures account: ")
        for key in self.futures_account.account:
            print("exchange: " + key)
            for i in self.futures_account.account[key]:
                print("object: " + i)
                for j in self.futures_account.account[key][i]:
                    print("action: {}, price: {}, value: {}".
                          format(j['action'],
                                 j['price'],
                                 j['value']))