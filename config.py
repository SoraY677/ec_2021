'''
全体に関する設定をするファイル
'''

from src.util import const


# テストモードの真偽
const.IS_TEST = True 

# ベースコマンド
if const.IS_TEST:
	const.BASE_COMMAND = ["python","test/windows/syn_pop.py"]
else:
	const.BASE_COMMAND = [] # FIXME: 適切なコマンド

# 解提出時の各パラメータ
const.FUNCTION_ID = "[1]"
const.CITY_ID = "hakodate"
const.SEEDS_ID = "[123,42,256]"

# 最適解の探索を分析する用のファイル
const.ANALYZE_OPTIMAZE_SOLUTION = 'analyze/OptimalSolution-graph'

# 解探索手法に関する定数
const.SEARCH_MAX = 100 # 解探索数の限界
const.POPLATION_MAX = 2 # 解集団数
const.EVOLVE_THRESHOLD = 0.05 # 二つの解の類似度を用いた進化をする際に使用する閾値
const.MULATION_THRESHOLD = 0.8 # 突然変異する閾値