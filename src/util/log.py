'''
ログを作成管理スクリプト
'''
import sys
from logging import getLogger, StreamHandler, handlers, Formatter
from logging import INFO, DEBUG, WARN, ERROR

from . import const

# ログの対象レベル
# DEBUG, INFO, WARN, ERROR　から選択
const.LOG_LEVEL = INFO

# ログをファイル出力するか否か
const.IS_LOG_OUTPUT = True

# ログの設定
logger = getLogger('build_log')

if const.IS_LOG_OUTPUT:
    handler = \
        handlers.RotatingFileHandler(
            r'build.log',
            mode='w',
            encoding='utf-8',
            backupCount=3
        )
else:
    handler = StreamHandler()
# フォーマットルール  
#  -> ex) 
#    [INFO]     log.py      [def]info       line.10     'test info':
#    sample massage show!
formatter = Formatter('[%(levelname)s]\t\t\n%(message)s')

handler.setLevel(const.LOG_LEVEL)
handler.setFormatter(formatter)
logger.setLevel(const.LOG_LEVEL)
logger.addHandler(handler)


def info(log_str):
    '''
    ログレベル:info記録

    Args:
    - log_str (str): 書き込む文字列
    '''
    logger.info(str(log_str))


def debug(log_str):
    '''
    ログレベル:debug記録

    Args:
    - log_str (str): 書き込む文字列
    '''
    logger.debug(str(log_str))


def warn(log_str):
    '''
    ログレベル:warn記録

    Args:
    - log_str (str): 書き込む文字列
    '''
    logger.warn(str(log_str))


def error(log_str):
    '''
    ログレベル:warn記録

    Args:
    - log_str (str): 書き込む文字列
    '''
    logger.error(str(log_str))
    sys.exit(1)

