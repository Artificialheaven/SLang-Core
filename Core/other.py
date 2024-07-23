# 本函数用于定义一些必要函数
import time


global_dict = {}


class Registers:
    func_dict = {}

    def __init__(self):
        print('Create Func Descriptor...')

    def __call__(self) -> dict:
        return self.func_dict

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
            print(f'函数{func.__name__}作为{name}被注册，参数{parma_len}个，介绍：{info}。')
            return wapperB
        return wapperA

    def call(self, func_name: str, parma: list, _dict: dict):
        if func_name in self.func_dict:
            ret = self.func_dict[func_name]['func'](parma, _dict)
            return ret
        else:
            # print(f'调用了不存在的函数{func_name}')
            return None

    def reg_not_callable(self, name, parma_len, info):
        self.func_dict[name] = {'name': name, 'func': None, 'parma_len': None, 'info': None}
        self.func_dict[name]['parma_len'] = parma_len
        self.func_dict[name]['info'] = info
        print(f'逻辑函数作为{name}被注册，参数{parma_len}个，介绍：{info}。')


class globals:
    _dict = {}

    def __call__(self) -> dict:
        return self._dict

    def get(self, key):
        try:
            return self._dict[key]
        except Exception as e:
            print(f'获取全局变量{key}时出现错误，error=>{e}')

    def add(self, key, value):
        self._dict[key] = value


__dict = {'glo': globals(), 'reg': Registers()}


def get_glo() -> globals:
    return __dict['glo']


def get_reg() -> Registers:
    return __dict['reg']
