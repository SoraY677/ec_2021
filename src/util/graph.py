from os import path

from . import const

optimal_solution_list = []
max_optimal = 0

def _add_optimal_solution2list(res_list):
	'''
	評価値をリストに追加

	Args:
		res_list (list): 1世代における評価値のリスト
	'''
	global optimal_solution_list
	global max_optimal
	for i in range(len(res_list)):
		max_optimal = res_list[i]['objective'] if(max_optimal < res_list[i]['objective']) else max_optimal
	optimal_solution_list.append(max_optimal)

def _create_optimal_solution_data_file():
	'''
	評価値をデータファイルに記録
	'''
	global optimal_solution_list
	with open(path.join(const.ANALYZE_OPTIMAZE_SOLUTION, 'data.json'), 'w') as f:
		f.write(str(optimal_solution_list))

def update_create_optimal_solution_data_file(res_list):
	'''
	評価値を更新
	世代交代時に実行される想定

	Args:
		res_list (list): 1世代における評価値のリスト
	'''
	_add_optimal_solution2list(res_list)
	_create_optimal_solution_data_file()
