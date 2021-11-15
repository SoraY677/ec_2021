'''
解探索スクリプト
人工蜂コロニーアルゴリズム
'''
import sys
sys.path.append('../')
from util import const
from util import log

const.EVOLVE_THRESHOLD = 0.05

def challenge_evolve():
    '''
    解を受け取り、解に少し変更を加えて新たな解を生成
    '''
    pass

def tracking_evolve(prudent_sol, prudent_eval, aggresive_sol,aggresive_eval):
    '''
    二つの解を比較し、類似度があまりに低く、
    積極派の解が慎重派の解より点数が高い場合はTrue、低い場合はFalse

    Args:
    - prudent_sol (dict): 慎重派の解
    - prudent_eval (int): 慎重派の評価
    - aggresive_sol (dict): 積極派の解
    - aggresive_eval (int): 積極派の評価

    Returns:
    - Boolean:  解が全く違う => True
                解が似ている => False
    '''

    # 類似度計算
    hist_ratio = 1
    hist_ratio *= hist_2num(prudent_sol[const.PAYMENT_NAME], aggresive_sol[const.PAYMENT_NAME])
    for key in const.ATTRIBUTE_NAME_LIST:
        hist_ratio *= hist_2array(prudent_sol[key], aggresive_sol[key]) 
    log.debug('類似度:' + str(hist_ratio))

    # 類似度が閾値を超えたら
    if hist_ratio < const.EVOLVE_THRESHOLD:
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
    # https://mieruca-ai.com/ai/jaccard_dice_simpson/
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
