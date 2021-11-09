'''
解の生成及びその過程で必要となる処理フローの定義

'''
import sys
import common
from copy import copy 
from random import shuffle, randint

sys.path.append('../')
from util import const
from util import log


def create_init_sol():
    '''
    解を生成する
    '''
    result = {}

    # 給付金額を決定
    result[const.PAYMENT_NAME] = 5 

    # 各属性に対してランダムで属性を取得するという処理
    attr_i = 1
    for attr_key in const.ALL_ATTRIBUTE_DICT:
        log.debug('A'+str(attr_i))
        target = []  # 対象として決定した配列を入れておく場所
        # 対象属性の配列をシャッフル
        copy_attr_array = list(const.ALL_ATTRIBUTE_DICT[attr_key])
        shuffle(copy_attr_array)
        # 解とする属性数をランダムで決定し取得
        select_attr_num = randint(1, len(copy_attr_array))
        target = copy(copy_attr_array[0:select_attr_num])
        log.debug('first-create:' + str(target))
        # 制約条件チェックを走らせ不要分を配列に追加
        lack_attr = tuple(common.get_need_attr(target, attr_i))
        
        log.debug('lack:' + str(lack_attr))
        for attr in lack_attr:
            if type(attr) is tuple:
                target.append(attr[randint(0,len(attr)-1)])
            else:
                target.append(attr)

        target.sort()
        log.debug('result:' + str(target))
        # 最終的な生成解の属性要素
        result[attr_key] = copy(target)
        attr_i += 1
        log.debug('==========================')

    return result



