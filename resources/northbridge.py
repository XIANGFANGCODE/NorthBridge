from flask_restful import Resource, reqparse, abort
from resources.alpha import Alpha
from resources.account import Account
from resources.evaluator import Evaluator
from common.scaffold import *

class NorthBridge(Resource):

    def makemoney(self, config, args):
        dc = {'message' : 'make money'}
        return dc

    def do_history_transaction(self, config, args):
        """
        历史回测
        :param args:
        :return:
        """
        if args is None:
            raise RuntimeError('args is none')
        ret = self.__excute('test', config, args)
        return ret

    def __excute(self, mode, config, args):
        """
        交易执行函数
        :param mode:  test: 历史回测
                      real: 真实市场交易
        :param args:
        :return:
        """
        evaluator = Evaluator()
        alpha = Alpha(mode)
        signals = alpha.moving_average(short_num=config['moving_average_short'],
                                       long_num=config['moving_average_long'],
                                       object=args['object'],
                                       exchange=args['exchange'])
        if len(signals) == 0:
            logging.info("There is no signals!")
            return evaluator

        account = Account(mode)
        account.get_account(exchange=args['exchange'],
                            datetime=signals[0].datetime,   # 从第一个信号开始
                            object='ustd',
                            start_account=config['start_account'])



