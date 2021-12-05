'''
処理のブロックごとに関数で分けたスクリプト
'''


from . import submit 
from .util import log
from .solution_search import population

def create():
    '''
    解を生成
    '''
    population.create()

def evaluate():
    '''
    解の評価

    Args:
    - base_command (list[str]): 基本コマンド
    '''

    # 解集団をまとめて評価するためのラッパー関数
    def submit_pop(sol_pop):
        for sol in sol_pop:
            submit.regist(sol)
        return submit.run()


    population.evaluate(submit_pop)

def evolove( ):
    '''
    解を進化させる
    '''
    population.evolve()
