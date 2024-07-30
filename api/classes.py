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
    del parma[0]
    if len(parma)%2 != 0:
        del parma[len(parma)-1]
    d = {}
    is_key = True

    for i in range(len(parma)):
        if is_key:
            d[parma[i]] = None
        else:
            d[parma[i-1]] = parma[i]
        is_key = not is_key

    _dict[name] = d
