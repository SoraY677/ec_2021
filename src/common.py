'''
定数値を定義するスクリプト
アッパースネークケースを採用

[ex] 
const.SAMPLE_DEFINE = True
'''

from util import const

# 家族類型
const.FAMILY_TYPE_ID = (
    0,   # 単独世帯
    1,   # 夫婦のみ世帯
    2,   # 夫婦と子供世帯
    3,   # 男親と子供
    4,   # 女親と子供
    50,  # 男親と両親 (夫の親)
    60,  # 夫婦とひとり親 (夫の親)
    70,  # 夫婦・子供と両親 (夫の親)
    80   # 夫婦・子供とひとり親 (夫の親)
)

# 世帯内役割
const.ROLE_HOUSEHOLD_TYPE_ID = (
    0,   # 単独世帯 (男性)
    1,   # 単独世帯 (女性)
    10,  # 夫・男親
    11,  # 妻・女親
    20,  # 子供 (男性)
    21,  # 子供 (女性)
    30,  # 親 (男性)
    31   # 親 (女性)
)

# 産業分類
const.INDUSTRY_TYPE_ID = (
    -1,  	# 非就業者
    10,  	# A 農業，林業
    20,  	# B 漁業
    30,  	# C 鉱業，採石業，砂利採取業
    40,  	# D 建設業
    50,  	# E 製造業
    60,  	# F 電気・ガス・熱供給・水道業
    70,  	# G 情報通信業
    80,  	# H 運輸業，郵便業
    90,  	# I 卸売業，小売業
    100,  # J 金融業，保険業
    110,  # K 不動産業，物品賃貸業
    120,  # L 学術研究，専門・技術サービス業
    130,  # M 宿泊業，飲食サービス業
    140,  # N 生活関連サービス業，娯楽業
    150,  # O 教育，学習支援業
    160,  # P 医療，福祉
    170,  # Q 複合サービス事業
    180,  # R サービス業 (他に分類されないもの)
    190,  # S 公務 (他に分類されるものを除く)
    200,  # T 分類不能の産業
)

# 雇用形態
const.EMPLOYMENT_TYPE_ID = (
    -1,  # 非就業者
    10,  # 一般労働者
    20,  # 短時間労働者
    30,  # 臨時労働者
)

# 企業規模
const.COMPANY_SIZE_ID = (
    -1,  		# 非就業者
    5,  		# 5~9人
    10,  		# 10~99人
    100,  	# 100~999人
    1000,  	# 1000人以上
)
