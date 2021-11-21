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
	# 各属性の値を整形
	
	attr_str = " and ".join(["{0} == {1}".format(str(key),str(sol[key]).replace(' ','')) for key in const.ATTRIBUTE_KEY_LIST])


	# コマンドに沿うように配列でラップ
	# ex) "family_type_id == [0,3,4,60,70,80] and role_household_type_id == [0,1,21,30,31] and industry_type_id == [-1,10,20,30,50,60,80,90,100,160,170,200] and employment_type_id == [-1,20,30] and company_size_id == [-1,5,10]" 9 "[2]" hakodate "[123,42,256]"
	return [str(attr_str), str(sol[const.PAYMENT_KEY]), str(sol[const.FUNCTION_ID_KEY]), str(sol[const.CITY_KEY]), str(sol[const.SEEDS_KEY])] 

def _sol_decode(eval_str):
	'''
	評価値(文字列)を分解して、関数内で扱える形に整形

	Args:
	- eval (str): 評価値(文字列)

	Returns:
	- list: 結果の配列
	'''
	return eval(eval_str)

def regist(sol = None, base_command = None):
	'''
	解提出用にコマンド登録を行う

	Args:
	- sol (dist): 解となる辞書
	- base_command(list): # 基本となるコマンド部分(argを除く)
	'''
	global _command_list

	# コマンドを作成
	command = base_command 
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

	return result_list[0]

_init() # 初期化しておく

