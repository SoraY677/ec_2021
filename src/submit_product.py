
import json
from subprocess import check_output
import subprocess

from .util import const
from .util import log

_input_list = None

def _init():
	'''
	初期化処理
	'''
	global _input_list
	_input_list = []

def _sol_encode(sol):
	res = {}
	res["query"] = " and ".join(["{0} == {1}".format(str(key),str(sol[key]).replace(' ','')) for key in const.ATTRIBUTE_KEY_LIST])
	res["payment"] = sol[const.PAYMENT_KEY]
	log.info('sol:' + '[payment] ' + str(res['payment']) + ' / [query] ' + str(res['query'] ))
	return res

def _sol_decode(eval_arg):
	res = {}
	# 戻り値
	eval_result = json.loads(eval_arg)

	feasible = True

	for constraint_item in eval_result['constraint']:
		if constraint_item > 0 : feasible = False

	# 目的関数が一つ
	if const.FUNCTION_ID_LEN == 1:
		res['objective'] = eval_result['objective'] if feasible is True else 1
		res['feasible'] = feasible
		res['info'] = eval_result['info']

	# 目的関数が二つ
	else:	
		res['objective'] = eval_result['objective'][0] * eval_result['objective'][1] if feasible is True else 1
		res['feasible'] = feasible
		res['objective-list'] = [eval_result['objective'][0], eval_result['objective'][1]]
		res['info'] = eval_result['info']

	log.info('response result:' + str(res))
	return res

def regist(sol):
	global  _input_list

	# コマンドを作成
	_input_list.append(_sol_encode(sol)) 

def run():
	global  _input_list
	result_list = []
	subprocess_list = []
	if bool(len(_input_list)):
		_input_list = tuple(_input_list)
		
		for input in _input_list:
			command = ['echo',str(input).replace('\'','"'),'|']
			command.extend(const.BASE_COMMAND)
			command = ' '.join(command)
			subprocess_list.append(subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  shell=True))
		
		for proc in subprocess_list:
			result = proc.communicate()[0]
			log.debug(result)
			result_list.append(_sol_decode(result))

		for proc in subprocess_list:
			proc.terminate()
	_init()
	
	return result_list

_init()