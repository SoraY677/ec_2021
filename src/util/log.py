'''
ログを作成管理スクリプト
'''
import sys

from logging import getLogger, StreamHandler, handlers
from logging import INFO, DEBUG, WARN, ERROR


# ログの対象レベル
# DEBUG, INFO, WARN, ERROR　から選択
LOG_LEVEL = DEBUG

# ログをファイル出力するか否か
IS_LOG_OUTPUT = True

# ログの設定
logger = getLogger('build_log')

if IS_LOG_OUTPUT:
    handler = \
        handlers.RotatingFileHandler(
            r'build.log',
            mode='w',
            encoding='utf-8',
            backupCount=3
        )
else:
    handler = StreamHandler()

handler.setLevel(LOG_LEVEL)
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)


def info(log_str):
    '''
    ログレベル:info記録

    Args:
    - log_str (str): 書き込む文字列
    '''
    logger.info('INFO:' + str(log_str))


def debug(log_str):
    '''
    ログレベル:debug記録

    Args:
    - log_str (str): 書き込む文字列
    '''
    logger.debug('DEBUG:' + str(log_str))


def warn(log_str):
    '''
    ログレベル:warn記録

    Args:
    - log_str (str): 書き込む文字列
    '''
    logger.warn('WARN:' + str(log_str))


def error(log_str):
    '''
    ログレベル:warn記録

    Args:
    - log_str (str): 書き込む文字列
    '''
    logger.error('ERROR:' + str(log_str))
    sys.exit(1)


# example
if __name__ == "__main__":
    info("sample")
