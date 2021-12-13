'''
解全体の管理を行うスクリプト
- 解探索に用いられる変数全体の保持
- 解探索中の各処理をまとめる
'''

from random import randint

from . import creater
from . import evolution
from ..util import const
from ..util import log
from ..util import graph

const.SEARCH_STYLE_PRUDENT = 0 # 探索のスタイルが慎重派 (小さく変化)
const.SEARCH_STYLE_AGGRESSIVE = 1 # 探索のスタイルが積極派 (大きく変化)

sol_poplation = [] # 解の集合
eval_poplation = [] # 解の評価値の集合 = 添え字番号を解の集合と合わせる

def create():
	'''
	解集団の新規生成
	'''
	for _ in range(const.POPLATION_MAX):
		sol_item = creater.create_init_sol()
		sol_poplation.append(sol_item)

		log.debug('create-solution:' + str(sol_item))

	log.debug('======================')

def evaluate(ex_eval_func):
	'''
	呼び出し元から受け取った評価関数をもとに、各解を評価

	Args:
	- ex_eval_func (def): 評価関数
	'''
	global sol_poplation, eval_poplation
	eval_poplation = ex_eval_func(sol_poplation)
	graph.update_create_optimal_solution_data_file(sol_poplation, eval_poplation)

def evolve():
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
				log.info('chase-happen! :' + str(j * 2) + '->' + str(i * 2 + 1))
				sol_poplation[i * 2] = sol_poplation[j * 2 + 1]
				is_tracking[j * 2] = True

	# 解を変化する
	for i in range(len(sol_poplation)):
			if i % 2 == 0:
				sol_poplation[i] = evolution.challenge_evolve_prudent(sol_poplation[i],eval_poplation[i]['feasible'])
			else:
				sol_poplation[i] = evolution.challenge_evolve_agressive(sol_poplation[i])
	

