'''
解全体の管理を行うスクリプト
- 解探索に用いられる変数全体の保持
- 解探索中の各処理をまとめる
'''

from random import random, randint
from copy import copy

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
	is_tracking = [False for _ in range(const.POPLATION_MAX)] # 既に1進化内で追従されていた場合のフラグ
	aggresive_pop = [{'pop':sol_poplation[i*2+1],'eval':eval_poplation[i*2+1]} for i in range(int(const.POPLATION_MAX/ 2))]

	# 評価値をもとにしたバブルソート
	for i in range(len(aggresive_pop)):
		for j in range(i+1, len(aggresive_pop)):
			if aggresive_pop[i]['eval']['objective'] > aggresive_pop[j]['eval']['objective']:
				aggresive_pop[i], aggresive_pop[j] = \
					aggresive_pop[j].copy(), aggresive_pop[i].copy()

	# 積極派解の評価 > 慎重派解の評価 ならば
	# 解を合わせる
	for i in range(int(len(aggresive_pop))):
		target_index = randint(0, int(const.POPLATION_MAX/2) - 1)
		# まだ追従済みではなく
		if is_tracking[target_index*2] is False:
			# 評価値的に交換する価値があれば
			if aggresive_pop[i]['eval']['objective'] < eval_poplation[target_index*2]['objective'] :
				sol_poplation[target_index*2] = aggresive_pop[i]['pop'].copy()
				is_tracking[target_index*2] = True


	# 解を変化する
	for i in range(len(sol_poplation)):
		if i % 2 == 0:
			sol_poplation[i] = evolution.challenge_evolve_prudent(sol_poplation[i],eval_poplation[i]['feasible'])
		else:
			sol_poplation[i] = evolution.challenge_evolve_agressive(sol_poplation[i])
	

