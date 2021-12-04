'''
- 解探索に用いられる変数全体の保持
- 解探索中の各処理をまとめる
'''
from . import create
from . import evolution

from random import randint


from ..util import const
from ..util import log

const.SEARCH_STYLE_PRUDENT = 0 # 探索のスタイルが慎重派 (小さく変化)
const.SEARCH_STYLE_AGGRESSIVE = 1 # 探索のスタイルが積極派 (大きく変化)

const.SEARCH_DIRECTION_PLUS = 1 # 探索の際に属性や金額を増やす方向で動く
const.SEARCH_DIRECTION_MINUS = -1 # 探索の際に属性や金額を増やす方向で動く

sol_poplation = []
eval_poplation = []

def create_sol(create_num, function_id, city, seeds):
	'''
	解の生成

	Args:
	- create_num (int, optional): . 生成する解の数 / Defaults : 0.
	'''
	for i in range(create_num):
		sol_item = create.create_init_sol(function_id, city, seeds)

		log.debug('create-solution:' + str(sol_item))

		sol_poplation.append(sol_item)
	log.debug('======================')


def evaluate_sol(ex_eval_func):
	'''
	呼び出し元から受け取った評価関数をもとに、各解を評価

	Args:
	- ex_eval_func (def): 評価関数
	'''
	global eval_poplation
	eval_poplation = ex_eval_func(sol_poplation)


def evolve_sol():
	'''
	解を進化させる
	'''
	is_tracking = [False for _ in range(const.POPLATION_MAX)]


	# 積極派解の評価 > 慎重派解の評価 であり
	# 積極派の解と慎重派の解の差がかなり開いていた場合は
	# 解を合わせる
	for i in range(int(len(sol_poplation) / 2)):
		for j in range(int(len(sol_poplation) / 2)):
			if not is_tracking[j * 2] and \
			evolution.tracking_evolve(
			sol_poplation[j * 2], 
			eval_poplation[j * 2]['objective'],
			sol_poplation[i * 2 + 1],
			eval_poplation[i * 2 + 1]['objective']) :
				sol_poplation[i * 2] = sol_poplation[j * 2 + 1]
				is_tracking[j * 2] = True

	# 解を変化する
	for i in range(len(sol_poplation)):
		if is_tracking[i] is False:
			if i % 2 == 0:
				sol_poplation[i] = evolution.challenge_evolve_prudent(sol_poplation[i],eval_poplation[i]['feasible'])
			else:
			 	sol_poplation[i] = evolution.challenge_evolve_agressive(sol_poplation[i])

			

	log.info('evolve after:' + str(sol_poplation))

	pass
	

