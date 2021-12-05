# 🧭環境構築

##  バージョン
3.7 <= `$ python --version` <= 3.9  

##  パッケージインストール
詳しくはrequirements.txtに記載。  
以下を実行。  
`$ pip install -r requirements.txt`

# 🔨ビルド手順
## 下準備

- configの確認

`<projectPath>/config.py`に解探索に関する主な設定が記載されているため要確認  

おそらく変更が必要となるのは以下の通り。  
```python
const.FUNCTION_ID = "[1]"
const.CITY_ID = "hakodate"
const.SEEDS_ID = "[123,42,256]"
```

## 実行

最適解の探索を行うコマンド
```bash
$ python main.py
```

# 🧰分析ツール


- 不要なファイル・ディレクトリの削除
```bash
$ python tool.py -clean
```

- 分析用Web立ち上げ
```bash
$ python tool.py -analyze
```  
-> 立ち上げ後: http://localhost:8000

- help
```bash
$ python tool.py -help
```

## 起動方法

TODO  

# UML

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