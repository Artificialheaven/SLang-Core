# SLang-Core
基于Python的文本处理语言

# Core
api 文件夹下创建文件可以修改以添加新的功能，格式如下
```python
from Core.register import Router


router = Router()

@router.reg('这里写函数名，不需要和下面的那个函数名一样，可以是中文', 1, '这里写函数简介，在启动时会列出')  # 第二个参数数字是参数个数，没啥用，不会妨碍被调用。
def name(parma: list, _dict: dict):  # name按照python标准命名即可，parma是传入的参数，按顺序传入，都是文本。_dict是当前运行的字典，一个Slang对象有唯一一个，可以修改或读取。
    pass  #在这里写下你的代码，只能返回 None 或者 字符串。（不使用return，如果有返回值，返回return时需要返回字符串，否则会报错）
```

在 regs.py 内导入你想要加入的代码
```python
from api.test import router as test_router
# 导入你的文件

register.set_router(test_router)
# 把导入的文件添加到全局解释器中，你也可以像 regs.py 创建新的解释器。
```

# 调用Slang
```python
Core.init.init()    # 这里进行初始化，只需要进行一次，不要多次进行。
Slang = Core.main.Slang(d={'debugging': True})  # 生成一个Slang对象，d是欲处理字典，只有本对象可以访问
Slang.run_room('【调试输出【变量debugging】】') # 运行Slang文本，返回最终的返回值。
```
示例Slang代码
```Slang
【调试输出你好，世界】【调试输出当前debug状态：【获取变量debug】】
```

# 引用Slang-Core
示例如main.py

# 需要库[仅支持Python39及以上]
```
requests
```
