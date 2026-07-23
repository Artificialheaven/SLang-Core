import time
from .globals import global_var


globals = global_var


class Router:
    """函数路由——装饰器注册 + 调用分发 + 多路由合并。"""

    def __init__(self):
        self.func_dict = {}

    def reg(self, name, parma_len, info):
        """装饰器——用中文名注册一个可调用函数。"""
        def wapperA(func):
            def wapperB(*args, **kwargs):
                t1 = time.time()
                ret = func(*args, **kwargs)
                t2 = time.time()
                print(f'调用{func.__name__}，用时{int((t2 - t1) * 1000)}ms。')
                return ret

            self.func_dict[name] = {
                'name': func.__name__,
                'func': func,
                'parma_len': parma_len,
                'info': info,
            }
            return wapperB

        return wapperA

    def call(self, func_name: str, parma: list, _dict: dict):
        """通过中文名调用一个已注册函数。"""
        if func_name in self.func_dict:
            return self.func_dict[func_name]['func'](parma, _dict)
        else:
            print(f'调用了不存在的函数{func_name}')
            return None

    def reg_not_callable(self, name, parma_len, info):
        """注册一个不可调用的逻辑函数（如控制流），由解释器直接处理。"""
        self.func_dict[name] = {
            'name': name,
            'func': None,
            'parma_len': parma_len,
            'info': info,
        }

    def set_router(self, router: 'Router'):
        """合并另一个 Router 的函数字典。同名函数保留已有注册。"""
        for name, entry in router.func_dict.items():
            if name in self.func_dict:
                continue
            self.func_dict[name] = entry

    def get_func_dict(self):
        return self.func_dict
