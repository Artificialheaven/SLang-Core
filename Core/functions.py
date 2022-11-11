import Core.other


'''
@Core.other.get_reg().reg('', 1, '')
def name(parma:list, _dict: dict):
    pass
'''


@Core.other.get_reg().reg('调试输出', 1, '控制台输出调试文本')
def debug_print(parma: list, _dict: dict):  # 所有的function都只有一个列表参数，接受文本传入的全部参数
    print(parma[0])


@Core.other.get_reg().reg('修改变量', 2, '修改SLang-Core全局变量')
def update_globals(parma: list, _dict: dict):
    Core.other.get_glo().add(parma[0], parma[1])


@Core.other.get_reg().reg('获取变量', 1, '获取SLang-Core全局变量')
def update_globals(parma: list, _dict: dict):
    # print(f'尝试获取全局变量{parma[0]}')
    return str(Core.other.get_glo().get(parma[0]))


@Core.other.get_reg().reg('删除变量', 1, '删除SLang-Core全局变量')
def del_var(parma:list, _dict: dict):
    do_not_delete = ('debug')
    if parma[0] in do_not_delete:
        print('禁止删除SLang-Core核心全局变量')
    else:
        del Core.other.get_glo()()[parma[0]]


@Core.other.get_reg().reg('赋值变量', 2, '赋值临时变量')
def set_room_var(parma:list, _dict: dict):
    _dict[parma[0]] = parma[1]


@Core.other.get_reg().reg('变量', 1, '获取临时变量')
def set_room_var(parma:list, _dict: dict):
    return str(_dict[parma[0]])



