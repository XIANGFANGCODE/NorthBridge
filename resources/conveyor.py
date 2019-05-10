from flask_restful import Resource, reqparse, abort
from resources.northbridge import NorthBridge
from common.scaffold import *

parser = reqparse.RequestParser()
parser.add_argument('action', required=True, help="Tell me what should i do?") #行为
parser.add_argument('alpha') #策略
parser.add_argument('risk') #风险
parser.add_argument('cost') #成本
parser.add_argument('order') #订单
parser.add_argument('execute') #执行
parser.add_argument('object') #标的
parser.add_argument('exchange') #交易所

class Conveyor(Resource):

    def __init__(self):
        """
        application入口
        """
        self.config = parse_config()    #解析配置文件
        format_logging(self.config)     #设置日志格式

    def put(self):
        args = parser.parse_args()
        if hasattr(NorthBridge(), args['action']):
            f = getattr(NorthBridge(), args['action'])
            return f(config=self.config, args=args)
        else:
            abort(404, message="{} action doesn't exist".format(args['action']))
