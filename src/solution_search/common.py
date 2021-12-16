'''
基本事項定義
'''
from copy import copy
from random import randint

from ..util import const
from ..util import log

# キー属性の定義
const.ATTRIBUTE_KEY_LIST = (
    'family_type_id',
    'role_household_type_id',
    'industry_type_id',
    'employment_type_id',
    'company_size_id'
)
const.PAYMENT_KEY = 'payment'
const.FUNCTION_ID_KEY = 'function_id'
const.CITY_KEY = 'city'
const.SEEDS_KEY = 'seeds'


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

# 各種別の属性配列
const.ALL_ATTRIBUTE_DICT = {
    'family_type_id': const.FAMILY_TYPE_ID,
    'role_household_type_id': const.ROLE_HOUSEHOLD_TYPE_ID,
    'industry_type_id': const.INDUSTRY_TYPE_ID,
    'employment_type_id': const.EMPLOYMENT_TYPE_ID,
    'company_size_id': const.COMPANY_SIZE_ID
}

# 制約条件として使用する条件リスト
const.CONTRAINT_ARRAY_LIST = \
    (
        (0, 4, 3),
        ((0, 1), ),
        (-1,),
        (-1, (20, 30), 10),
        (-1, 5, 10, 100, 1000)
    )

def get_need_attr(cur_list: list, attr_id:int):
    '''
    指定の配列(各属性)に対して、制約条件に当てはめて足りていない属性を返す

    Args:
    - cur (list): 検索対象とする属性の配列
    - context_id (int): 属性種別A1 ~ A5の番号部分 (1 ~ 5)以外の指定はエラー
        - A1: 家族類型
        - A2: 世帯内役割
        - A3: 産業分類
        - A4: 雇用形態
        - A5: 企業規模​
    '''
    try:
        if type(cur_list) is not list:
            log.warn('引数のタイプが違う')
            raise TypeError

        result = []

        # 渡された配列
        target_array = copy(cur_list)

        # 制約条件となる配列
        # 優先度が x > y    となる場合は (x, y)
        # 優先度が x, y > z となる場合は ((x, y), z)
        # という構成
        if 1 <= attr_id <= 5:
            constraint_array = const.CONTRAINT_ARRAY_LIST[attr_id - 1]
        else:
            log.warn('attr_id wrong')
            raise Exception(attr_id)

        # 渡された配列のサイズがそもそも0
        if len(target_array) == 0:
            if type(constraint_array[0]) is tuple:
                result = [constraint_array[0][randint(0,len(constraint_array[0]) - 1)]]
            else:
                result = [constraint_array[0]]

        # 配列に何かしらの要素が入っている
        else:

            no_contain_array = []  # 含まれなかった優先度の要素
            need_contain_array_length = 0  # 不足分として対象にするべき要素の数

            # チェックループ
            for constraint_el in constraint_array:
                # 優先度が複数のもの
                if type(constraint_el) is tuple:
                    # 含まれているかチェック
                    for el in constraint_el:
                        if el in target_array:
                            need_contain_array_length = len(no_contain_array)
                            target_array.remove(el)
                        # 含まれていない要素は不足
                        else :
                            no_contain_array.append(el)

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
        

    return result

def get_complete_attr(cur_list_origin, key):
    '''
    現状の属性に不足していた分の要素を追加した完全な配列の取得

    Args:
    - cur_list_origin (list): 現状の属性配列
    - key (str): 対象の属性名

    Returns:
        list: 完成した属性の配列
    '''
    complete_list = copy(cur_list_origin)

    # 不足している分を現在の配列に追加する処理
    lack_attr = tuple(get_need_attr(complete_list, const.ATTRIBUTE_KEY_LIST.index(key) + 1))
    for attr in lack_attr:
        if type(attr) is tuple:
            complete_list.append(attr[randint(0,len(attr)-1)])
        else:
            complete_list.append(attr)

    complete_list.sort()

    return complete_list

def get_popable_attr(cur_list, key):
    '''
    現在のリストの属性をもとに削除できる要素を返す  
    ** 昇順にソートされた、正しい属性のみからなる配列及びキーを想定。エラーハンドリング欠如 **  

    Args:
    - cur_list (list): 現在の配列
    - key (str): 対象のキー

    Returns:
    - list: 削除することのできる属性の配列
    '''
    # そもそも何も入っていない場合は削除できる要素はない
    if len(cur_list) <= 1: return []

    list_copy = copy(cur_list)
    # 対象とする制約条件のリスト
    target_constraint_array = const.CONTRAINT_ARRAY_LIST[const.ATTRIBUTE_KEY_LIST.index(key)]

    # 制約条件を順に探索
    for i in range(len(target_constraint_array)):
        
        # 探索途中で全ての要素が削除されてしまった = 一つ前の要素が返せる要素
        if len(list_copy) == 0: result = list(target_constraint_array[i - 1])

        # 同優先度の制約条件の場合
        if type(target_constraint_array[i]) is tuple:
            result = []
            # 一つずつ制約条件を見ていく
            for constraint in target_constraint_array[i]:
                if constraint in list_copy:
                    result.append(constraint)
                    list_copy.pop(list_copy.index(constraint))
            if len(list_copy) == 0: return result

        # 単一の制約条件の場合は存在するか調べて、あれば削除
        else:
            if target_constraint_array[i] in list_copy:
                list_copy.pop(list_copy.index(target_constraint_array[i]))

            if len(list_copy) == 0:
                if  type(target_constraint_array[i]) is tuple:
                    return list(target_constraint_array[i])
                return [target_constraint_array[i]]

    return list(list_copy)

def get_appendable_attr(cur_list, key):
    '''
    追加可能な要素を取得
    ** 昇順にソートされた、正しい属性のみからなる配列及びキーを想定。エラーハンドリング欠如 **   

    Args:
    - cur_list (list): 現在の配列
    - key (str): 対象のキー

    Returns:
    - list: 追加することのできる属性の配列
    '''

    list_copy = copy(cur_list)

    target_constraint_array = const.CONTRAINT_ARRAY_LIST[const.ATTRIBUTE_KEY_LIST.index(key)]
    not_in_result_list = [] # 最終候補に入らないリスト

    for constraint in target_constraint_array:
        # 同優先度が複数ある要素
        if type(constraint) is tuple:
            result = []
            for constraint_item in constraint:
                # 含まれているならば候補から外す
                if constraint_item in list_copy:
                    not_in_result_list.append(constraint_item)
                    list_copy.pop(list_copy.index(constraint_item))
                # 含まれていなければそれが必要
                else:
                    result.append(constraint_item)

            if len(result) != 0:
                return result

        # 単一の制約条件
        else:
            # 含まれていた場合には要素削除
            if constraint in list_copy:
                not_in_result_list.append(constraint)
                list_copy.pop(list_copy.index(constraint))
            # 含まれていなければそれが必要
            else:
                return [ constraint ]

    not_in_result_list.extend(cur_list) # 現状のリストに含まれているその他要素に関しても候補から外す
    
    return [item for item in const.ALL_ATTRIBUTE_DICT[key] if item not in not_in_result_list]
    
