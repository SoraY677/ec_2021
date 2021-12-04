'''
解探索スクリプト
人工蜂コロニーアルゴリズム
'''
from random import random, randint, shuffle
from copy import copy

from types import new_class
from ..util import const
from ..util import log

from . import create
from . import common

const.EVOLVE_THRESHOLD = 0.05


def get_attr_noinclude_list(cur_list, attr_key):
    '''
    まだ含まれていない要素のリストを取得

    Args:
    - cur_list (list) : 現在の要素
    - attr_key (str): 属性のキー名
    '''

    diff = set(cur_list) ^  set(const.ALL_ATTRIBUTE_DICT[attr_key])
    return list(diff)


def challenge_evolve_prudent(sol, feasible):
    '''
    解に少し変更を加えて新たな解の生成を試みる

    Args:
    - sol [dict] : 現在の解情報
    - feasible [bool] : 実行可能解か否か -> True/False
    '''
    new_sol = copy(sol)

    # 解の評価結果が制約条件を満たしていない時
    if feasible == False:
        change_attr_max = randint(1,3)
        shuffle_list = copy(list(const.ATTRIBUTE_KEY_LIST))
        shuffle(shuffle_list)
        shuffle_list = shuffle_list[0:change_attr_max-1]
        for key in shuffle_list:
            if len(new_sol[key]) > 0 :
                new_sol[key].pop(randint(0, len(new_sol[key])-1))
                new_sol[key].pop(randint(0, len(sol[key])-1))
                lack_arr = common.get_need_attr(new_sol[key],const.ATTRIBUTE_KEY_LIST.index(key) + 1).copy()
                new_sol[key].extend(lack_arr)
                new_sol[key].sort()
        # 金額の変化
        if randint(0,100) < [80,50,30][3 - change_attr_max]:
            new_sol[const.PAYMENT_KEY] /= random() + 1
            new_sol[const.PAYMENT_KEY] = round(new_sol[const.PAYMENT_KEY], 5)
    
    # 解の評価結果が制約条件を満たしている
    else :
        change_attr_max = randint(1,5)
        for _ in range(change_attr_max):
            target_key = const.ATTRIBUTE_KEY_LIST[randint(0,len(const.ATTRIBUTE_KEY_LIST) - 1)]
            # 50%で要素増加
            if randint(0, 100) > 50:
                noinclude_list = get_attr_noinclude_list(new_sol[target_key], target_key)
                
                if len(noinclude_list) > 0:
                    new_sol[target_key].append(noinclude_list[randint(0,len(noinclude_list)-1)])
            # 残り50%で要素削減
            else:
                new_sol[target_key].pop(randint(0, len(sol[target_key])-1))
                lack_arr = common.get_need_attr(new_sol[target_key], const.ATTRIBUTE_KEY_LIST.index(target_key) + 1).copy()
                new_sol[target_key].extend(lack_arr)
            
            new_sol[target_key].sort()

        # 金額の変化        
        new_sol[const.PAYMENT_KEY] /= random() * 2 + 0.000001
        new_sol[const.PAYMENT_KEY] = round(new_sol[const.PAYMENT_KEY], 5)


    log.info('new_sol:' + str(new_sol))
    return new_sol

def challenge_evolve_agressive(sol):
    '''
    解を大幅に変化

    Args:
    - sol (dict): 解情報

    Returns:
    - dict: 新規解情報
    '''

    new_sol = copy(sol)
    # 完全ランダム再生成
    if random() > 0.8:
        new_sol = create.create_init_sol(const.FUNCTION_ID, const.CITY_ID, const.SEEDS_ID)

    else:
        change_attr_max = randint(1,15)
        for _ in range(change_attr_max):
            target_key = const.ATTRIBUTE_KEY_LIST[randint(0, len(const.ATTRIBUTE_KEY_LIST) - 1)]
            # 50%で要素を追加
            if randint(0, 100) > 50:
                noinclude_list = get_attr_noinclude_list(new_sol[target_key], target_key)
                if len(noinclude_list) > 0:
                    new_sol[target_key].append(noinclude_list[randint(0,len(noinclude_list)-1)])
            # 残り50%で要素削減
            else:
                if len(sol[target_key]) > 0 :
                    new_sol[target_key].pop(randint(0, len(sol[target_key])-1))

            # 不足分を補う
            lack_arr = common.get_need_attr(new_sol[target_key], const.ATTRIBUTE_KEY_LIST.index(target_key) + 1).copy()
            new_sol[target_key].extend(lack_arr)
            new_sol[target_key].sort()

    
        for _ in range(5):
            new_sol[const.PAYMENT_KEY] /= random() * 2 + 0.000001
            new_sol[const.PAYMENT_KEY] = round(new_sol[const.PAYMENT_KEY], 5)

    return new_sol



def tracking_evolve(prudent_sol, prudent_eval, aggresive_sol,aggresive_eval):
    '''
    二つの解を比較し、類似度があまりに低く、
    積極派の解が慎重派の解より点数が高い場合はTrue、低い場合はFalse

    Args:
    - prudent_sol (dict): 慎重派の解
    - prudent_eval (int): 慎重派の評価
    - aggresive_sol (dict): 積極派の解
    - aggresive_eval (int): 積極派の評価

    Returns: Boolean  
    - 解が全く違う => True
    - 解が似ている => False
    '''

    # 類似度計算
    hist_ratio = 1
    hist_ratio *= hist_2num(prudent_sol[const.PAYMENT_KEY], aggresive_sol[const.PAYMENT_KEY])
    for key in const.ATTRIBUTE_KEY_LIST:
        hist_ratio *= hist_2array(prudent_sol[key], aggresive_sol[key]) 
    log.info('類似度:' + str(hist_ratio))

    # 類似度が閾値を超えたら
    if hist_ratio < const.EVOLVE_THRESHOLD:
        if prudent_eval < aggresive_eval:
            return True

    return False


def hist_2num(number_a, number_b):
    '''
    二つの値の類似度を算出する

    Args:
        number_a (int): 比較元数値
        number_b (int): 比較先数値
    '''

    return (20 - abs(number_a - number_b)) / 20


def hist_2array(list_a, list_b):
    '''
    二つの解の類似度を各項目ごとに算出

    Args:
    sol_1 (dict): 比較元配列
    sol_2 (dict): 比較先配列
    '''
    
    # DICE係数を用いる
    # https://mieruca-ai.com/ai/jaccard_dice_simpson/ より拝借
    # *各要素のDICE係数を掛け合わせ総合類似度を計算
    
    # 集合Aと集合Bの積集合(set型)を作成
    set_intersection = set.intersection(set(list_a), set(list_b))
    #集合Aと集合Bの積集合の要素数を取得
    num_intersection = len(set_intersection)
 
    #集合Aの要素数を取得
    num_listA = len(list_a)
    #集合Bの要素数を取得
    num_listB = len(list_b)
 
    #定義式に従い，Dice係数を算出
    try:
        return float(2.0 * num_intersection) / (num_listA + num_listB)
    except ZeroDivisionError:
        return 1.0 
