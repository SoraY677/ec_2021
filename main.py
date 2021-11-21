import time
from src.util import const 
from src.util import log

from src import process


const.SEARCH_MAX = 3 # 解探索限界で定義
const.POPLATION_MAX = 1 # 扱う解集合の数を定義
const.FUNCTION_ID = "[1,2]"
const.CITY_ID = "hakodate"
const.SEEDS_ID = "[123,42,256]"



if __name__ == "__main__":

	# タイマー計測開始
	start_time = time.time()

	# 解の生成
	process.create_sol(const.POPLATION_MAX, const.FUNCTION_ID, const.CITY_ID, const.SEEDS_ID)
	loop_num = const.SEARCH_MAX / const.POPLATION_MAX

	for _ in range(int(loop_num)):
		# 解の評価
		process.evaluate_sol(base_command=["python","test/windows/syn_pop.py"])

		# 最良解の探索
		pass

	# タイマー計測終了
	end_time = time.time()

	log.info('経過時間:' + str(end_time - start_time) )





