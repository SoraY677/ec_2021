'''
処理のブロックごとに関数で分けたスクリプト
'''
from .util import log
from .solution_search import population
from . import submit 

def create_sol(sol_max = 0, function_id=None, city=None, seeds=None):
    '''
    解を生成

    Args:
    - sol_max (int): 解の生成数
    '''

    ### エラーハンドリング
    if sol_max <= 0:
        log.error("create_solの引数はsol_maxは「> 0」でなければならない。")
    elif function_id is None or \
         city is None or\
         seeds is None:
        log.error('create_solにおける引数の指定が足りません！')

    population.create_sol(sol_max, function_id, city, seeds)

def evaluate_sol(base_command = []):
    '''
    解の評価

    Args:
    - base_command (list[str]): 基本コマンド
    '''
    ### エラーハンドリング
    # リストであること
    if not isinstance(base_command, list):
        log.error("「base_command = list型」である必要があります。")
    # コマンドの指定があること
    elif len(base_command) == 0:
        log.error("base_commandに何も入っていません")

    # 解集団をまとめて評価するためのラッパー関数
    def submit_pop(sol_pop):
        for sol in sol_pop:
            submit.regist(sol['solution'], base_command)
        return submit.run()


    population.evaluate_sol(submit_pop)

def evolove_sol( ):
    '''
    解を進化させる
    '''
    population.evolve_sol()
