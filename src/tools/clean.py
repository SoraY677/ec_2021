
import os
import shutil

def run():
	'''
	不要なファイル・ディレクトリを削除
	'''

	# 削除対象のファイル名・フォルダ名
	clean_target = (
		'__pycache__',
		'data.json',
		'build.log'
	)

	def recursive_file_check(path):
		'''
		ディレクトリのネストを下げて最下層まで探す再帰関数

		Args:
		- path (str): 探索地点のディレクトリパス
		'''
		for target in clean_target:
			# 対象のファイルを発見
			if  os.path.isfile(path):
				if target in path:
					os.remove(path)

			# 対象のディレクトリを発見
			elif target in path:
				shutil.rmtree(path)

			# 対象では無ければより深くへ
			else :
				files = os.listdir(path)
				for file in files:
					recursive_file_check(path + "\\" + file)
		
	recursive_file_check('.') # プロジェクトの最上位層から全探索
