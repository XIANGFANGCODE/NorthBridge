import logging

class Account:
    """
    资金账户类，用以现实所有的资产
    数据模型为一个2级字典，value = dict[exchange][object]
    结构如下
        {
            "tushare" : {
                "ustd" : "100",
                "btc" : "1",
                "eth" : "2"
            },
            "huobi" : {
                "ustd" : "1000",
                "btc" : "2",
                "eth" : "3"
            }
        }
    """
    def __init__(self, mode):
        self.mode = mode
        self.account = dict()
        self.datetime = ""

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
            self.account = self._get_test_account(exchange, object, start_account)
        elif self.mode == 'real':
            self.account = self._get_real_account(exchange)
        else:
            logging.error("account has no mode {}.".format(self.mode))
        return self

    def _get_test_account(self, exchange, object, start_account):
        self.account[exchange] = dict()
        self.account[exchange][object] = start_account
        return self.account

    def _get_real_account(self, exchange):
        return self.account

    def desc(self):
        print("mode: {}, datetime: {}".format(self.mode, self.datetime))
        for key in self.account:
            print("exchange: " + key)
            for i in self.account[key]:
                print("object: {}, value: {}".format(i, self.account[key][i]))
