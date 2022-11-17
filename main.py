import Core.init
import Core.main


# 这个地方实际上会先运行基础的init，例如globals和reg的注册
Core.init.init()    # 这里进行初始化检测
Slang = Core.main.Slang(d={'debugging': True})
text = input('>>>')
Slang.run_room(text)
