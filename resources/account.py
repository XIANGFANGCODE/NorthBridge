class Account:
    """
    资金账户类，用以现实所有的资产
    """
    def __init__(self, config, mode, exchage):
        """
        为一个2级字典，value = dict[exchange][object]
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
        :param mode:  账户类型： test、real
        :param exchage: 交易所
        """
        self.account = dict()
        if mode == 'test':
            self.account[exchage] = dict()
            self.account[exchage]['ustd'] = config['start_account']
        else:
            # TODO 通过交易获取所有交易所的账户信息
            pass
