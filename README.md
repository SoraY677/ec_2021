# 🧭環境構築

##  バージョン
3.7 <= `$ python --version` <= 3.9  

##  パッケージインストール
詳しくはrequirements.txtに記載。  
以下を実行。  

```bash
pip install -r requirements.txt
```
# 🔨ビルド手順
## 下準備

- `config.py`の確認

`<projectPath>/config.py`を作成し、解探索に関する設定を記載する必要がある

```python
from src.util import const

# テストモードの真偽
const.IS_TEST = True 

# ベースコマンド
if const.IS_TEST:
	const.BASE_COMMAND = ["python","test/windows/syn_pop.py"]
else:
	const.BASE_COMMAND = []

# 提出時のパラメータのうち、リスト内に複数パターンとして固定できる物の定義
const.FUNCTION_ID_LIST = ["[1]","[2]","[1,2]"]
const.CITY_ID_LIST = ["naha","hakodate"]

# 解提出時の各パラメータ
const.FUNCTION_ID = const.FUNCTION_ID_LIST[0] # **変更可能**
const.CITY_ID = const.CITY_ID_LIST[0] # **変更可能**
const.SEEDS_ID = "[123,42,256]"

# 最適解の探索を分析する用のファイル
const.ANALYZE_OPTIMAZE_SOLUTION = 'analyze'

# 解探索手法に関する定数
const.SEARCH_MAX = 100 # 解探索数の限界
const.POPLATION_MAX = 10 # 解集団数
const.EVOLVE_THRESHOLD = 0.05 # 二つの解の類似度を用いた進化をする際に使用する閾値
const.MULATION_THRESHOLD = 0.8 # 突然変異する閾値
```

現在はテストモードのみの対応である。

## 実行

最適解の探索を行うコマンド
```bash
python main.py
```

# 🧰分析ツール


- 不要なファイル・ディレクトリの削除
```bash
python tool.py -clean
```

- 分析用Web立ち上げ
```bash
python tool.py -analyze
```  
-> 立ち上げ後: http://localhost:8000

- help
```bash
python tool.py -help
```

# 📋UML

## モジュール依存関係

```
                                    |
                                    | [allAccessable]
          +---------+               |
       +->| main.py |               |  +-----------+
       |  +---------+               |  | common.py |
       |                            |  +-----------+
+------+-----+   +------------+     |
| process.py |<--+ submit.py  |     |  +-----------+
+------^-----+   +------------+     |  | config.py |
       |                            |  +-----------+
+------+--------+                   |
| population.py |<-------+          |   +----------+
+------^--------+        |          |   | const.py |
       |                 |          |   +----------+
 +-----+------+  +-------+------+   |
 | creater.py |  | evolution.py |   |    +--------+
 +------------+  +--------------+   |    | log.py |
                                    |    +--------+
                                    |
                                    |
```
