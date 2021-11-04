"""
定数定義可能なスクリプト
コードの説明は省略(詳しくは引用元参照)

[使用方法]
```
import const

const.FOO = 100			# OK
const.BAR = 'Hello'	# OK
const.FOO = 200  		# NG 
```

[引用]
-> [python recipes](https://code.activestate.com/recipes/414140-constant-types-in-python/)
"""


import sys


class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


sys.modules[__name__] = _const()
