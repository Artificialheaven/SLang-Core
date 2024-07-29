from Core.register import Register
from Core.functions import register as main_router

from api.test import router as test_router
from api.classes import router as classes_router


register = Register()
register.set_router(main_router)

register.set_router(test_router)
register.set_router(classes_router)

