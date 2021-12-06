'''
並列処理をするためのThread用スクリプト
'''
import subprocess

from copy import copy

from .util import const
from .util import log

# コマンド一式が入る配列
_command_list = None

def _init():
	'''
	初期化処理
	'''
	global _command_list
	_command_list = []

def _sol_encode(sol):
	'''
	解を提出できる形に整形

	Args:
	- sol (dist): 解の辞書

	Returns:
	- str: 提出する解の文字列つなぎ
	'''
	res = None

	# クエリーを生成
	query = " and ".join(["{0} == {1}".format(str(key),str(sol[key]).replace(' ','')) for key in const.ATTRIBUTE_KEY_LIST])

	
	if const.IS_TEST:
		res = [str(query), str(sol[const.PAYMENT_KEY]), str(sol[const.FUNCTION_ID_KEY]), str(sol[const.CITY_KEY]), str(sol[const.SEEDS_KEY])] 

	else:
		res = {}
		res['query'] = str(query)
		res['payment'] = sol[const.PAYMENT_KEY]


	return res 

def _sol_decode(eval_arg):
	'''
	評価値(文字列)を分解して、関数内で扱える形に整形

	Args:
	- eval_arg (str): 評価値

	Returns:
	- list: 結果の配列
	'''
	res = {}


	if const.IS_TEST:
		eval_result = eval(eval_arg)
		# 目的関数が一つ
		if const.FUNCTION_ID_LEN == 1:
			res['objective'] = 0 if eval_result[0] is None else eval_result[0]
			res['feasible'] = False if eval_result[0] is None else True
			res['info'] = eval_result[1]
		# 目的関数が二つ
		else:
			res['objective'] = [eval_result[0], eval_result[2]]
			res['objective'][0] = 0 if res['objective'][0] is None else res['objective'][0]
			res['objective'][1] = 0 if res['objective'][1] is None else res['objective'][1]
			res['feasible'] = eval_result[4]
			res['info'] = [eval_result[1], eval_result[3]]

	else: # TODO: 本番環境に投げた際の物だが、おそらくうまくいかないので、後で直すこと
		res['objective'] = eval_arg['objective']

		# マイナスの値があったら実行不可能解
		isFeasible = True
		for con in eval_arg['constraint']:
			if con < 0:
				isFeasible = False
			
		res['feasible'] = isFeasible
		res['info'] = eval_arg['info']

	log.info('response result:' + str(res))
	return res

def regist(sol = None):
	'''
	解提出用にコマンド登録を行う

	Args:
	- sol (dist): 解となる辞書
	- base_command(list): # 基本となるコマンド部分(argを除く)
	'''
	global _command_list

	# コマンドを作成
	command = const.BASE_COMMAND.copy() 
	command.extend(_sol_encode(sol))
	log.info('create command:' + str(command))
	# コマンドリストに追加
	_command_list.append(command)
	

def run():
	'''
	並列実行する
	'''
	global _command_list

	subprocess_list = []
	result_list = []
	# 処理対象に何か入っていれば
	if bool(len(_command_list)):
		_command_list = tuple(_command_list)
		# 並列処理を実行する
		for command in _command_list:
			subprocess_list.append(subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
		subprocess_list = tuple(subprocess_list)
		# 全てのプロセスが終了するまでの待機
		for proc in subprocess_list:
			result = proc.communicate()[0]
			log.debug(result)
			result_list.append(_sol_decode(result))

		for proc in subprocess_list:
			proc.terminate()

	# 全ての処理が終了したら最初の状態に戻す
	_init()

	return result_list

_init() # 初期化しておく

