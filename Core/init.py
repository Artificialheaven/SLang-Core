import Core.other
import Core.functions


def init():
    Core.other.get_glo().add('debug', False)
    # print('debug状态：', Core.other.get_glo().get('debug'))
    Core.other.get_reg().call('调试输出', ["\033[1;30;47m高性能しぶそうしん機 !!\033[0m"], {})
