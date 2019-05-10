import tushare as ts
import sys
sys.path.append("..")
from common.scaffold import *
from os import path
import pandas as pd

def get_btc_pricevol_by_tushare(start_date='20000101', end_date='20200101'):
    """
    通过tushare获取比特币每日量价
    注意每次tushare最多返回1000行，因此需要循环处理
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 返回文件链接
    """
    config = parse_config()
    ts.set_token(config['tushare_token'])
    pro = ts.pro_api()
    start_year = int(start_date[0:4])
    end_year = int(end_date[0:4])
    df = pd.DataFrame()
    while start_year <= end_year:
        df = df.append(pro.query('btc_pricevol',
                       start_date = str(start_year) + '0101',
                       end_date = str(start_year) + '1231'))
        start_year += 1
    df = df.sort_values('date')
    file = path.join(path.dirname(path.dirname(path.realpath(__file__))),'data','digital_cash','btc_history_from_tushare.csv')
    df.to_csv(file)
    return file



