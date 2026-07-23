# Core运行器
from Core.ast import parse, evaluate
from Core.register import Router


class Slang:
    """SLang 解释器对象。

    每个 Slang 实例拥有独立的：
    - _dict:     局部变量字典
    - register:  函数注册表（通常与全局共享）
    """

    _dict = {}

    def __init__(self, register: Router, d=None):
        if d is None:
            d = {}
        self._dict = d
        self.register = register
        # 缓存已知函数名集合，用于 AST 解析时的函数名消歧
        self._known_names = set(register.get_func_dict().keys())

    def __call__(self, text: str, d=None):
        """便捷调用：运行文本后返回自身。"""
        if d is not None:
            self._dict = d
        self.run_room(text)
        return self

    def get_dict(self) -> dict:
        """获取当前局部变量字典。"""
        return self._dict

    def run_room(self, text: str) -> str:
        """解析 Slang 文本为 AST 并求值。

        两阶段处理：
        1. parse(text, known_names)  → AST 节点列表
        2. evaluate(nodes, self)     → 递归求值

        :param text: Slang 语言文本实体
        :return: 处理后的结果字符串
        """
        # 预处理：允许用户用换行和缩进排版长代码
        # 1. 逐行 strip 后拼接（消除每行缩进）
        # 2. 清理 >=< 分隔符两侧残留空白（双重保险）
        import re
        lines = text.split('\n')
        text = ''.join(line.strip() for line in lines)
        text = re.sub(r'\s*>=\<\s*', '>=<', text)
        try:
            nodes = parse(text, self._known_names)
            return evaluate(nodes, self)
        except Exception as e:
            print('ERROR: ')
            print(e)
            return ''
