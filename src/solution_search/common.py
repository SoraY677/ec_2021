'''
定数値を定義するスクリプト
アッパースネークケースを採用

[ex]
const.SAMPLE_DEFINE = True
'''


import sys
from copy import copy
from typing import List

sys.path.append('../')
from util import const
from util import log

const.ATTRIBUTE_NAME_LIST = (
    'family_type_id',
    'role_house_type_id',
    'industry_type_id',
    'employment_type_id',
    'company_size_id'
)

# 家族類型
const.FAMILY_TYPE_ID = (
    0,   # 単独世帯
    1,   # 夫婦のみ世帯
    2,   # 夫婦と子供世帯
    3,   # 男親と子供
    4,   # 女親と子供
    50,  # 男親と両親 (夫の親)
    60,  # 夫婦とひとり親 (夫の親)
    70,  # 夫婦・子供と両親 (夫の親)
    80   # 夫婦・子供とひとり親 (夫の親)
)

# 世帯内役割
const.ROLE_HOUSEHOLD_TYPE_ID = (
    0,   # 単独世帯 (男性)
    1,   # 単独世帯 (女性)
    10,  # 夫・男親
    11,  # 妻・女親
    20,  # 子供 (男性)
    21,  # 子供 (女性)
    30,  # 親 (男性)
    31   # 親 (女性)
)

# 産業分類
const.INDUSTRY_TYPE_ID = (
    -1,  	# 非就業者
    10,  	# A 農業，林業
    20,  	# B 漁業
    30,  	# C 鉱業，採石業，砂利採取業
    40,  	# D 建設業
    50,  	# E 製造業
    60,  	# F 電気・ガス・熱供給・水道業
    70,  	# G 情報通信業
    80,  	# H 運輸業，郵便業
    90,  	# I 卸売業，小売業
    100,    # J 金融業，保険業
    110,    # K 不動産業，物品賃貸業
    120,    # L 学術研究，専門・技術サービス業
    130,    # M 宿泊業，飲食サービス業
    140,    # N 生活関連サービス業，娯楽業
    150,    # O 教育，学習支援業
    160,    # P 医療，福祉
    170,    # Q 複合サービス事業
    180,    # R サービス業 (他に分類されないもの)
    190,    # S 公務 (他に分類されるものを除く)
    200,    # T 分類不能の産業
)

# 雇用形態
const.EMPLOYMENT_TYPE_ID = (
    -1,  # 非就業者
    10,  # 一般労働者
    20,  # 短時間労働者
    30,  # 臨時労働者
)

# 企業規模
const.COMPANY_SIZE_ID = (
    -1,  	# 非就業者
    5,  	# 5~9人
    10,  	# 10~99人
    100,  	# 100~999人
    1000,  	# 1000人以上
)

const.ALL_ATTRIBUTE_DICT = {
    'family_type_id': const.FAMILY_TYPE_ID,
    'role_household_type_id': const.ROLE_HOUSEHOLD_TYPE_ID,
    'industry_type_id': const.INDUSTRY_TYPE_ID,
    'employment_type_id': const.EMPLOYMENT_TYPE_ID,
    'company_size_id': const.COMPANY_SIZE_ID
}


def get_need_attr(array: list, attr_id):
    '''
    指定の配列(各属性)に対して、制約条件に当てはめて足りていない属性を返す

    Args:
    - array (list): 検索対象とする属性の配列
    - context_id (int): 属性種別A1 ~ A5の番号部分 (1 ~ 5)以外の指定はエラー
        - A1: 家族類型
        - A2: 世帯内役割
        - A3: 産業分類
        - A4: 雇用形態
        - A5: 企業規模​
    '''
    try:
        if type(array) is not list:
            raise TypeError

        result = []

        # 渡された配列
        target_array = copy(array)

        # 制約条件となる配列
        # 優先度が x > y    となる場合は (x, y)
        # 優先度が x, y > z となる場合は ((x, y), z)
        # という構成
        constraint_array = ()

        if attr_id == 1:
            # 単独世帯 > 女親と子供 > 男親と子供 > その他
            constraint_array = (0, 4, 3)
        elif attr_id == 2:
            # 単独世帯(男性)，単独世帯(女性) > その他
            constraint_array = ((0, 1), )
        elif attr_id == 3:
            # 非就業者 > その他
            constraint_array = (-1,)
        elif attr_id == 4:
            # 非就業者 > 短時間労働者，臨時労働者 > 一般労働者
            constraint_array = (-1, (10, 20), 30)
        elif attr_id == 5:
            # 非就業者 > 5〜9人 > 10~99人 > 100~999人 > 1000人以上
            constraint_array = (-1, 5, 10, 100, 1000)
        else:
            raise Exception

        # 渡された配列のサイズがそもそも0
        if len(target_array) == 0:
            result = [constraint_array[0]]

        # 配列に何かしらの要素が入っている
        else:

            no_contain_array = []  # 含まれなかった優先度の要素
            need_contain_array_length = 0  # 不足分として対象にするべき要素の数

            # チェックループ
            for constraint_el in constraint_array:
                # 優先度が複数のもの
                if type(constraint_el) is tuple:
                    is_either_contain = False  # どちらかが含まれているフラグ
                    # どちらかが含まれているかチェック
                    for el in constraint_el:
                        if el in target_array:
                            is_either_contain = True
                            need_contain_array_length = len(no_contain_array)
                            target_array.remove(el)
                    # どちらの要素も含まれていない場合は要素不足
                    if is_either_contain is False:
                        no_contain_array.append(constraint_el)

                # 優先度が単一のもの
                else:
                    if constraint_el not in target_array:
                        no_contain_array.append(constraint_el)
                    else:
                        need_contain_array_length = len(no_contain_array)
                        target_array.remove(constraint_el)

            # 満たされていない制約条件がある状態で、
            # まだ調査対象に要素が残っている場合
            if len(no_contain_array) != 0 and len(target_array) != 0:
                need_contain_array_length = len(no_contain_array)
            # 戻り値に清算
            no_contain_array = tuple(no_contain_array)
            for i in range(need_contain_array_length):
                result.append(no_contain_array[i])

    except Exception as e:
        log.error(e)
        pass

    return result

