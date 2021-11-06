'''
ログを作成管理スクリプト
'''
from logging import getLogger, StreamHandler
from logging import INFO, DEBUG, WARN, ERROR

# ログレベルの辞書
LOG_LEVEL_LIST = {'INFO': INFO, 'DEBUG': DEBUG, 'WARN': WARN, 'ERROR': ERROR}
# ログレベルの文字列リスト
LOG_LEVEL_STR_LIST = ('INFO', 'DEBUG', 'WARN', 'ERROR')


class Log:
    '''
    ログの管理をするクラス
    '''

    logger = None

    def __init__(self, log_level_str=LOG_LEVEL_STR_LIST[0]):
        '''
        初期化

        Args:
        - log_level_str (str, optional): 指定するログレベルの文字列. Defaults to LOG_LEVEL_STR_LIST[0]('INFO').

        Raises:
        - Exception: 指定のログレベルが存在しない場合のエラー
        '''

        self.logger = getLogger(__name__)
        try:
            if log_level_str in LOG_LEVEL_STR_LIST:
                log_level = LOG_LEVEL_LIST[log_level_str]
                handler = StreamHandler()
                handler.setLevel(log_level)
                self.logger.setLevel(log_level)
                self.logger.addHandler(handler)
            else:
                raise Exception("指定したログレベルが存在しませんでした!")
        except Exception as e:
            self.logger.error(e)
            exit()

    def info(self, str):
        '''
        ログレベル:info記録

        Args:
        - str (str): 書き込む文字列
        '''
        self.logger.info(str)

    def debug(self, str):
        '''
        ログレベル:debug記録

        Args:
        - str (str): 書き込む文字列
        '''
        self.logger.debug(str)

    def warn(self, str):
        '''
        ログレベル:warn記録

        Args:
        - str (str): 書き込む文字列
        '''
        self.logger.warn(str)

    def error(self, str):
        '''
        ログレベル:warn記録

        Args:
        - str (str): 書き込む文字列
        '''
        self.logger.error(str)


if __name__ == "__main__":
    log = Log('DEBU')
    log.debug("hoge")
