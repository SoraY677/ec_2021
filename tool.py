'''
便利なツール集
'''

import sys

from src.tools import clean, serve 

def help():
	'''
	ヘルプコマンド
	'''
	print('[command list]')
	for command in command_list:
		print(command)

# コマンドリスト
command_list = {
		'-help' : help,
		'-clean' : clean.run, 
		'-analyze' : serve.run
	}

if __name__ == '__main__':

	# 引数含めて正しい数になっていない
	if(len(sys.argv) is not 2):
		print('argv is only 1.if help command need, "python tool.py -help" ')
	
	else:
		is_command_found = False

		# 探索
		for key in command_list:
			if sys.argv[1] == key:
				is_command_found = True
				command_list[key]()

		# 引数が見つからなかった場合
		if is_command_found is False:
			print('argv not found. help command need, "python tool.py -help" ')

	