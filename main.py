from Core.init import init as slang_init

from regs import register
from Core.main import global_dict


# 这个地方实际上会先运行基础的init，例如globals和reg的注册
Slang = slang_init(register, d={'debugging': True})    # 这里进行初始化检测
global_dict['debug'] = True

try:
    while True:
        text = input('>>>')
        print(Slang.run_room(text))
except KeyboardInterrupt as e:
    print("\nUser Exit Slang")
    exit()
