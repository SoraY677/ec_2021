'''
並列処理をするためのThread用スクリプト
'''
import subprocess

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
	log.info('sol:' + '[payment] ' + str(sol[const.PAYMENT_KEY]) + ' / [query] ' + str(query))

	
	res = [str(query), str(sol[const.PAYMENT_KEY]), str(sol[const.FUNCTION_ID_KEY]), str(sol[const.CITY_KEY]), str(sol[const.SEEDS_KEY])] 

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


	eval_result = eval(eval_arg)
	# 目的関数が一つ
	if const.FUNCTION_ID_LEN == 1:
		res['objective'] = 1 if eval_result[0] is None else eval_result[0]
		res['feasible'] = False if eval_result[0] is None else True
		res['info'] = eval_result[1]
	# 目的関数が二つ
	else:
		
		res['objective'] = 1 if eval_result[0] is None or eval_result[2] is None else eval_result[0] * eval_result[2]
		res['feasible'] = False if eval_result[0] is None or eval_result[2] is None else True
		res['objective-list'] = [eval_result[0], eval_result[2]]
		res['info'] = [eval_result[1], eval_result[3]]

	log.info('response result:' + str(res))
	return res

def regist(sol):
	'''
	解提出用にコマンド登録を行う

	Args:
	- sol (dist): 解となる辞書
	'''
	global _command_list

	# コマンドを作成
	command = const.BASE_COMMAND.copy() 
	command.extend(_sol_encode(sol))
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

