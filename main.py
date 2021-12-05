import time

import config
from src import process
from src.util import const 
from src.util import log

if __name__ == "__main__":

	# タイマー計測開始
	start_time = time.time()

	# function_id の要素数を取得
	const.FUNCTION_ID_LEN = len(eval(const.FUNCTION_ID))

	# 解の生成
	process.create()
	loop_num = const.SEARCH_MAX / const.POPLATION_MAX

	for _ in range(int(loop_num)):
		# 解の評価
		process.evaluate()

		# 進化
		process.evolove()

	# タイマー計測終了
	end_time = time.time()

	log.info('経過時間:' + str(end_time - start_time) )





