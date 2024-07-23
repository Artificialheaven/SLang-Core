import Core.other
import Core.functions
from Core.register import Register


globals_dict = Core.other.global_dict


def init(register: Register):
    #globals_dict.add('debug', False)
    # 在这里注册 not callable 类函数，逻辑函数
    register.reg_not_callable('判断', 3, '第一个参数为真时运行第二个参数，为假时运行第三个参数')
    register.reg_not_callable('比较-', 5, '第一个参数可为[大于|小于|等于|大于等于|小于等于|不等于]，比较对象为第二个和第三个，比较成立运行第四个参数，否则运行第五个')
    register.reg_not_callable('循环-', 2, '第一个参数为真时运行第二个参数，否则返回之前运行的全部返回值')
    print(f'共有{len(register.get_func_dict())}个函数被注册！')
    # print('debug状态：', Core.other.get_glo().get('debug'))
    register.call('调试输出', ["\033[1;30;47m高性能しぶそうしん機 !!\033[0m"], {})
