import configparser
import logging, logging.handlers
from os import path

def parse_config():
    """
    解析配置文件
    :return: 返回一个字典，包含所有的配置文件信息
    """
    config = dict()
    d = path.join(path.dirname(path.dirname(path.realpath(__file__))),'config','config') #获取当前文件所在目录
    if not path.exists(d):
        raise RuntimeError("config file is not exist")
    cf  = configparser.ConfigParser()
    cf.read(d)

    # tushare
    config['tushare_token'] = cf.get('tushare','tushare_token')

    # log
    config['logging_level'] = cf.get('logging','logging_level')

    # alpha
    config['moving_average_short'] = cf.get('alpha','moving_average_short')
    config['moving_average_long'] = cf.get('alpha','moving_average_long')


    return config


def format_logging(config):
    """
    配置日志类
    (a)要求将所有级别的日志都写入磁盘文件中
    (b)all.log文件中记录所有的日志信息
    (c)error.log文件中单独记录error及以上级别的日志信息
    (d)要求all.log，每秒一个log文件，超过10个log就删除。
    :param config:
    :return:
    """
    logger = logging.getLogger()
    logger.setLevel(config['logging_level'])
    f1 = logging.FileHandler(path.join(path.dirname(path.dirname(path.realpath(__file__))),'log','all.log'))
    f2 = logging.FileHandler(path.join(path.dirname(path.dirname(path.realpath(__file__))), 'log', 'error.log'))
    f2.setLevel(logging.ERROR)
    format1 = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s : %(message)s')
    format2 = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s : %(message)s')
    f1.setFormatter(format1)
    f2.setFormatter(format2)
    logger.addHandler(f1)
    logger.addHandler(f2)


def get_id(id_type):
    """
    TODO 需改为从数据sequence获取
    获取唯一的编号，供数据存储使用
    :param id_type: 需要的id类型
    :return: 返回一个id值
    """
    seq = 1
    return ID_TYPE[id_type] + 1


#定义各类常量
ID_TYPE = {
    'signal' : 1000000
}

TUSHARE_DATA_TYPE = {
    'seq' : 0,
    'date' : 1,
    'price' : 2,
    'volume' : 3
}