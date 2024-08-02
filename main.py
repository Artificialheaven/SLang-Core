from Core.init import init as slang_init
from regs import register


if __name__ == "__main__":
    # 这个地方实际上会先运行基础的init，例如globals和reg的注册
    Slang = slang_init(register, d={'debug': True})    # 这里进行初始化检测

    try:
        while True:
            text = input('>>>')
            print(Slang.run_room(text))
    except KeyboardInterrupt as e:
        print("\nUser Exit Slang")
        exit()
