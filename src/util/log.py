'''
ログを作成管理スクリプト
'''
from logging import getLogger, StreamHandler, handlers
from logging import INFO, DEBUG, WARN, ERROR

# ログの対象レベル
# DEBUG, INFO, WARN, ERROR　から選択
LOG_LEVEL = DEBUG

# ログをファイル出力するか否か
IS_LOG_OUTPUT = False

# ログの設定
logger = getLogger(__name__)

if IS_LOG_OUTPUT:
    handler = \
        handlers.RotatingFileHandler(
            r'log.txt',
            mode='w',
            encoding='utf-8',
            maxBytes=100,
            backupCount=3
        )
else:
    handler = StreamHandler()

handler.setLevel(LOG_LEVEL)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)


def info(str):
    '''
    ログレベル:info記録

    Args:
    - str (str): 書き込む文字列
    '''
    logger.info(str)


def debug(str):
    '''
    ログレベル:debug記録

    Args:
    - str (str): 書き込む文字列
    '''
    logger.debug(str)


def warn(str):
    '''
    ログレベル:warn記録

    Args:
    - str (str): 書き込む文字列
    '''
    logger.warn(str)


def error(str):
    '''
    ログレベル:warn記録

    Args:
    - str (str): 書き込む文字列
    '''
    logger.error(str)
