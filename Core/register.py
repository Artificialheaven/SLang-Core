import time
from .globals import global_var


globals = global_var


class Router:
    def __init__(self):
        self.func_dict = {}

    def reg(self, name, parma_len, info):
        def wapperA(func):
            def wapperB(*args, **kwargs):
                t1 = time.time()
                ret = func(*args, **kwargs)
                t2 = time.time()
                print(f'调用{func.__name__}，用时{int((t2 - t1) * 1000)}ms。')
                return ret

            self.func_dict[name] = {'name': func.__name__, 'func': func, 'parma_len': None, 'info': None}
            self.func_dict[name]['parma_len'] = parma_len
            self.func_dict[name]['info'] = info
            # print(f'函数{func.__name__}作为{name}被注册，参数{parma_len}个，介绍：{info}。')
            return wapperB

        return wapperA

    def call(self, func_name: str, parma: list, _dict: dict):
        if func_name in self.func_dict:
            ret = self.func_dict[func_name]['func'](parma, _dict)
            return ret
        else:
            return None

    def reg_not_callable(self, name, parma_len, info):
        self.func_dict[name] = {'name': name, 'func': None, 'parma_len': None, 'info': None}
        self.func_dict[name]['parma_len'] = parma_len
        self.func_dict[name]['info'] = info
        # print(f'逻辑函数作为{name}被注册，参数{parma_len}个，介绍：{info}。')

    def get_func_dict(self):
        return self.func_dict


class Register:
    def __init__(self):
        self.func_dict = {}

    def reg(self, name, parma_len, info):
        def wapperA(func):
            def wapperB(*args, **kwargs):
                t1 = time.time()
                ret = func(*args, **kwargs)
                t2 = time.time()
                print(f'调用{func.__name__}，用时{int((t2 - t1) * 1000)}ms。')
                return ret

            self.func_dict[name] = {'name': func.__name__, 'func': func, 'parma_len': None, 'info': None}
            self.func_dict[name]['parma_len'] = parma_len
            self.func_dict[name]['info'] = info
            # print(f'函数{func.__name__}作为{name}被注册，参数{parma_len}个，介绍：{info}。')
            return wapperB

        return wapperA

    def call(self, func_name: str, parma: list, _dict: dict):
        if func_name in self.func_dict:
            ret = self.func_dict[func_name]['func'](parma, _dict)
            return ret
        else:
            print(f'调用了不存在的函数{func_name}')
            return None

    def reg_not_callable(self, name, parma_len, info):
        self.func_dict[name] = {'name': name, 'func': None, 'parma_len': None, 'info': None}
        self.func_dict[name]['parma_len'] = parma_len
        self.func_dict[name]['info'] = info
        # print(f'逻辑函数作为{name}被注册，参数{parma_len}个，介绍：{info}。')

    def set_router(self, router: Router):
        for i in router.func_dict:
            if i in self.func_dict:
                continue
            self.func_dict[i] = router.func_dict[i]
            d = router.func_dict[i]
            # print(f'函数{d["name"]}作为{i}被注册，参数{d["parma_len"]}个，介绍：{d["info"]}。')


    def get_func_dict(self):
        return self.func_dict



