'''
解の生成及びその過程で必要となる処理フローの定義
'''
from copy import copy 
from random import shuffle, randint

from . import common
from ..util import const
from ..util import log

def create_init_sol():
    '''
    初期の解を生成する

    Returns:
        dist: 生成した解
    '''
    result = {}

    # 給付金額を決定
    result[const.PAYMENT_KEY] = randint(1, 10) # FIXME: 値段の決め方

    # オプション
    result[const.FUNCTION_ID_KEY] = const.FUNCTION_ID
    result[const.CITY_KEY] = const.CITY_ID
    result[const.SEEDS_KEY] = const.SEEDS_ID


    # 各種別に対し、ランダムで属性を取得して、それぞれ配列にするという処理
    for key in const.ALL_ATTRIBUTE_DICT:
        target = []  # 最終的な配列

        # それぞれ種別が入った属性の配列をシャッフル
        copy_attr_array = list(const.ALL_ATTRIBUTE_DICT[key])
        shuffle(copy_attr_array)

        # 属性数をランダムで決定し、取得
        select_attr_num = randint(1, len(copy_attr_array))
        target = copy(copy_attr_array[0:select_attr_num])
        # 不足分を補って完成
        target = common.get_complete_attr(target, key)
        log.debug('result:' + str(target))
        # 最終的な生成解として登録
        result[key] = copy(target)

    return result

