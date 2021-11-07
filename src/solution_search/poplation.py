'''
- 解探索に用いられる変数全体の保持
- 解探索中の各処理をまとめる
'''
import sys
import create
from random import randint


sys.path.append('../')
from util import const
from util import log

const.SEARCH_STYLE_PRUDENT = 0 # 探索のスタイルが慎重派 (小さく変化)
const.SEARCH_STYLE_AGGRESSIVE = 1 # 探索のスタイルが積極派 (大きく変化)

const.SEARCH_DIRECTION_PLUS = 1 # 探索の際に属性や金額を増やす方向で動く
const.SEARCH_DIRECTION_MINUS = -1 # 探索の際に属性や金額を増やす方向で動く

sol_poplation = []

def create_sol(create_num = 10):
	'''
	解の生成

	Args:
		create_num (int, optional): . 生成する解の数 / Defaults : 10.
	'''
	for i in range(create_num):
		sol_item = {}
		# 初期の解
		sol_item['solution'] = create.create_init_sol()
		# 探索のスタイルを半分ずつで整形
		sol_item['style'] = (const.SEARCH_STYLE_PRUDENT , const.SEARCH_STYLE_AGGRESSIVE)[i % 2] 
		# 次に探索する際の属性と金額の増減設定
		sol_item['direction'] = (const.SEARCH_DIRECTION_PLUS, const.SEARCH_DIRECTION_MINUS)[randint(0,1)]

		log.debug('create-solution:' + str(sol_item))

		sol_poplation.append(sol_item)
	log.debug('======================')
	
		
