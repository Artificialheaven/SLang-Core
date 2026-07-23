import Core.functions
from Core.register import Router
import Core.main
from Core.globals import global_var as globals_dict


def init(register: Router, d) -> Core.main.Slang:
    """初始化 SLang 运行环境。

    注册三个控制流函数（判断 / 比较- / 循环-），
    这些函数在 AST 求值器中直接处理，不走 register.call()。
    """
    register.reg_not_callable('判断', 3, '第一个参数为真时运行第二个参数，为假时运行第三个参数')
    register.reg_not_callable('比较-', 5, '第一个参数可为[大于|小于|等于|大于等于|小于等于|不等于]，比较对象为第二个和第三个，比较成立运行第四个参数，否则运行第五个')
    register.reg_not_callable('循环-', 2, '第一个参数为真时运行第二个参数，否则返回之前运行的全部返回值')
    Slang = Core.main.Slang(register, d)
    return Slang
