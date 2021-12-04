import time
from src.util import const 
from src.util import log

from src import process

const.ANALYZE_OPTIMAZE_SOLUTION = 'analyze/OptimalSolution-graph'

const.isTest = True 

const.SEARCH_MAX = 100 # 解探索限界で定義
const.POPLATION_MAX = 2 # 扱う解集合の数を定義
const.FUNCTION_ID = "[1]"
const.CITY_ID = "hakodate"
const.SEEDS_ID = "[123,42,256]"



if __name__ == "__main__":

	# タイマー計測開始
	start_time = time.time()

	# function_id の要素数を取得
	const.FUNCTION_ID_LEN = len(eval(const.FUNCTION_ID))

	# 解の生成
	process.create_sol(const.POPLATION_MAX, const.FUNCTION_ID, const.CITY_ID, const.SEEDS_ID)
	loop_num = const.SEARCH_MAX / const.POPLATION_MAX

	for _ in range(int(loop_num)):
		# 解の評価
		process.evaluate_sol(base_command=["python","test/windows/syn_pop.py"])

		# 進化
		process.evolove_sol()

	# タイマー計測終了
	end_time = time.time()

	log.info('経過時間:' + str(end_time - start_time) )





