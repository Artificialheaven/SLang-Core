from Core.register import Router


router = Router()


@router.reg('置数组', 2, '生成一个数组对象')
def set_list(parma: list, _dict: dict):
    l = []
    name = parma[0]
    del parma[0]
    for i in parma:
        l.append(i)
    _dict[name] = l


@router.reg('置字典', 2, '生成一个字典对象')
def set_dict(parma: list, _dict: dict):
    name = parma[0]
    items = parma[1:]
    d = {}
    for i in range(0, len(items) - 1, 2):
        d[items[i]] = items[i + 1]
    _dict[name] = d
