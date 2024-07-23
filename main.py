import Core.init
import Core.main
from regs import register


# 这个地方实际上会先运行基础的init，例如globals和reg的注册
Core.init.init(register)    # 这里进行初始化检测
Slang = Core.main.Slang(register, d={'debugging': True})

try:
    while True:
        text = input('>>>')
        print(Slang.run_room(text))
except KeyboardInterrupt as e:
    print("\nUser Exit Slang")
    exit()
