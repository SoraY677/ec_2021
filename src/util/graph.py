from os import path
import json
from copy import copy

from . import const

# 最適解の評価値のみの記録
optimal_solution_eval_list = []
# 全ての解の記録
all_solution_list = []

min_optimal = 1

def _add_optimal_solution2list(submit_list, res_list):
	'''
	評価値をリストに追加

	Args:
	- submit_list(list) : 1世代における属性のリスト
	- res_list (list): 1世代における評価値のリスト
	'''
	global optimal_solution_eval_list
	global min_optimal
	global all_solution_list

	eval_list = []
	pop_list = []
	for i in range(len(res_list)):
		min_optimal = res_list[i]['objective'] if(min_optimal > res_list[i]['objective']) else min_optimal
		eval_list.append(res_list[i])
		pop_list.append(submit_list[i])

	optimal_solution_eval_list.append(min_optimal)
	all_solution_list.append({'pop_list':pop_list,'eval_list':eval_list})

def _create_optimal_solution_data_file():
	'''
	評価値をデータファイルに記録
	'''
	global optimal_solution_eval_list
	global all_solution_list

	with open(path.join(const.ANALYZE_OPTIMAZE_SOLUTION, 'data.json'), 'w') as f:
		json.dump({
			'optimal_solution_eval_list':optimal_solution_eval_list,
			'all_solution_list':all_solution_list
			},
			f, ensure_ascii=False)
def update_create_optimal_solution_data_file(submit_list ,res_list):
	'''
	評価値を更新
	世代交代時に実行される想定

	Args:
	- submit_list(list) : 1世代における属性のリスト
	- res_list (list): 1世代における評価値のリスト
	'''
	_add_optimal_solution2list(submit_list, res_list)
	_create_optimal_solution_data_file()
