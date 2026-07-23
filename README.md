# SLang-Core
基于Python的文本处理语言

## 架构

```
输入文本 ──parse()──▶ AST 节点列表 ──evaluate()──▶ 输出字符串
```

### 核心模块

| 模块 | 作用 |
|------|------|
| `Core/ast.py` | AST 节点定义 + 递归下降解析器 + 求值器 |
| `Core/main.py` | `Slang` 解释器对象 |
| `Core/register.py` | `Router` 函数注册/调用/合并 |
| `Core/functions.py` | 31 个内置函数（输出、变量、文本、网络、SQLite、配置等） |
| `Core/init.py` | 初始化：注册控制流函数 → 创建 Slang 实例 |
| `Core/globals.py` | 全局变量字典 |

### API 扩展

`api/` 文件夹下创建文件可以添加新功能：

```python
from Core.register import Router

router = Router()

@router.reg('函数名（中文也可）', 参数个数, '功能简介')
def my_func(parma: list, _dict: dict):
    # parma: 传入的参数列表，全部为字符串
    # _dict: 当前 Slang 对象的局部变量字典
    # 返回 None 或字符串
    pass
```

然后在 `regs.py` 中导入并注册：

```python
from api.my_module import router as my_router
register.set_router(my_router)
```

## 调用方式

```python
from Core.init import init as slang_init
from regs import register

Slang = slang_init(register, d={'debug': True})
result = Slang.run_room('【调试输出你好，世界】【获取变量debug】')
```

### REPL 交互

```bash
python main.py
>>>【调试输出你好，世界】
```

## Slang 语法

- 函数调用用 `【函数名 参数1>=<参数2>=<...】` 包围
- 参数分隔符为 `>=<`
- 支持嵌套调用：`【外层【内层参数】】`
- 真值: `True` / `true` / `真` / `1`
- 假值: `False` / `false` / `假` / `0`

### 控制流

- `【判断条件>=<真分支>=<假分支】`
- `【比较-大于>=<左值>=<右值>=<真分支>=<假分支】`（大于/小于/等于/大于等于/小于等于/不等于）
- `【循环-条件>=<循环体】`

## 依赖

```
requests
```

Python 3.9+
