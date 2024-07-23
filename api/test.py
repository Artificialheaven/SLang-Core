from Core.register import Router


router = Router()


@router.reg('test', 1, 'none')
def _test(parma: list, _dict: dict):
    print(parma[0])
