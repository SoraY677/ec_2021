import yaml

from .util import const


def init():
	with open('config.yml', 'r') as yml:
		config = yaml.load(yml)

	const.ANALYZE_OPTIMAZE_SOLUTION = config['ANALYZE_OPTIMAZE_SOLUTION']
	const.IS_TEST = True 

	const.SEARCH_MAX = 100 # 解探索限界で定義
	const.POPLATION_MAX = 2 # 扱う解集合の数を定義
	const.FUNCTION_ID = "[1]"
	const.CITY_ID = "hakodate"
	const.SEEDS_ID = "[123,42,256]"