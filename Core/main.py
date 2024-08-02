# Core运行器
# import Core._other
from Core.register import Register
from .globals import global_var as global_dict


class Slang:
    _dict = {}

    def __init__(self, register: Register, d=None):
        if d is None:
            d = {}
        self._dict = d
        self.register = register
        # 创建初始变量表

    def __call__(self, text: str, d=None):
        """
        :param text: 欲运行的Slang文本
        :param d: 欲植入的字典
        :return: 返回自身
        """
        if d is not None:
            self._dict = d
        self.run_room(text)
        return self

    def get_dict(self) -> dict:
        return self._dict

    def run_room(self, text: str) -> str:
        """
        :param text: Slang语言文本实体
        :return: 返回处理结束的语言
        """
        leftcount = 0
        isAbuild = False
        rightcount = 0
        startat = 0
        returnmsg = text
        # print(text)
        for i in range(len(text)):
            if text[i] == "【":
                # 说明可能触发了一个函数
                leftcount = leftcount + 1
                if not isAbuild:
                    # 函数房间启动位置
                    startat = i
                    # print(startat, ret[i])
                isAbuild = True
            elif text[i] == "】" and isAbuild:
                # 这是一个函数并且有 leftcount 次嵌套
                rightcount = rightcount + 1
            if rightcount == leftcount and isAbuild:
                # print(startat, i, text[startat:i + 1])
                # 只进行一次，将消息替换为返回值
                leftcount = 0
                rightcount = 0
                isAbuild = False
                ret = self.sample_run_room(text[startat:i + 1])
                # print(text[startat:i + 1], ret)
                if ret == None:
                    returnmsg = returnmsg.replace(text[startat:i + 1], '', 1)
                else:
                    returnmsg = returnmsg.replace(text[startat:i + 1], ret, 1)
                startat = 0
                # 初始化，为下一个函数房间做准备
                # text[startat:i + 1] : 单个运行的房间，一次性运行
        return returnmsg

    def sample_run_room(self, text: str):
        # 运行最小变量单元，应该先分割出各个层次的函数，然后由内从前向后运行
        # print(text)
        try:
            for i in self.register.get_func_dict():
                # print(text, '【'+i, text.startswith('【' + i))
                if text.startswith('【' + i):
                    # 确认当前运行函数名
                    # print(f'确认当前运行目标为：{i}')
                    dst = 0
                    _list = []
                    do = True
                    left_count = 0
                    for count in range(len(text)):
                        # 遍历测试寻找参数位置
                        if text[count] == '【' and count != 0:
                            do = False
                            left_count += 1
                            # 发现了嵌套函数
                        if text[count] == '】':
                            left_count -= 1
                        if left_count == 0:
                            do = True
                            # 内部左右括号平衡，继续获取参数
                        if text[count:count + 3] == '>=<' and do:
                            if dst == 0:
                                _list.append(text[len('【' + i):count])
                                # print('定位到第一个参数' + text[len('【' + i):count])
                            else:
                                _list.append(text[dst:count])
                                # print('定位到位于中部的参数' + text[dst:count])
                            dst = count + 3  # dst为定位前端
                        if len(_list) == 0 and count == len(text) - 1:
                            # 无参数的或者只有一个的
                            if not text == '【' + i + '】':
                                # 包含一个参数，把去掉首尾的【函数】去掉剩下的都是参数
                                _list.append(text[len('【' + i):len(text) - 1])
                                # print('定位到唯一参数' + text[len('【' + i):len(text)-1])
                        if not dst == 0 and do and text[count] == '】' and count == len(text) - 1:
                            _list.append(text[dst:len(text) - 1])
                            # print('定位到末尾参数' + text[dst:len(text)-1])

                    if i == '判断':   # 判断执行 参数1为逻辑，[True|真|1|true] 都视为真， [False|假|0|false] 视为假
                        # print(_list)
                        boolean = self.run_room(_list[0])   # list[0]为
                        if boolean in ['True', 'true', '真', '1']:   # 运行第二个参数
                            ret = self.run_room(_list[1])
                            return ret
                        elif boolean in ['False', 'false', '假', '0']:
                            ret = self.run_room(_list[2])
                            return ret
                        else:
                            print(f'运行 {text} 时发现异常，作为判断标准的函数异常，错误函数 {_list[0]} 其返回值 {boolean}')
                            if global_dict['debug']:   # 开启debug模式，以boolean作为返回值
                                return boolean
                            else:   # 未开启返回空
                                return ''
                    ifline = False
                    if i == '比较-':
                        # print(_list)
                        int_1, int_2 = self.run_room(_list[1]), self.run_room(_list[2])
                        # print(int_1, int_2)
                        if _list[0] == '大于':
                            if int_1 > int_2:
                                ifline = True
                        if _list[0] == '小于':
                            if int_1 < int_2:
                                ifline = True
                        if _list[0] == '等于':
                            if int_1 == int_2:
                                ifline = True
                        if _list[0] == '大于等于':
                            if int_1 >= int_2:
                                ifline = True
                        if _list[0] == '小于等于':
                            if int_1 <= int_2:
                                ifline = True
                        if _list[0] == '不等于':
                            if int_1 != int_2:
                                ifline = True
                        if ifline:
                            ret = self.run_room(_list[3])
                            return ret
                        else:
                            if len(_list) < 5:
                                # 不够五个参数，而且为不成立，那么不做任何运行
                                return ''
                            ret = self.run_room(_list[4])
                            return ret
                    if i == '循环-':
                        booleans = self.run_room(_list[0])
                        boolean = False
                        if booleans in ['True', 'true', '真', '1']:
                            boolean = True
                        else:
                            boolean = False
                        ret = ''
                        while boolean:
                            ret = ret + self.run_room(_list[1])
                            booleans = self.run_room(_list[0])
                            if booleans in ['True', 'true', '真', '1']:
                                boolean = True
                            else:
                                boolean = False
                        return ret

                    # print(_list)
                    if len(_list) != 0:
                        for j in range(len(_list)):
                            ret = self.run_room(_list[j])
                            # print(ret.find('【'))
                            while ret.find('【') != -1:
                                ret = self.run_room(_list[j])
                                # print('解析参数' + _list[j] + '返回', ret)
                            _list[j] = ret
                    # print(f'运行{i},{_list}')

                    ret = self.register.call(i, _list, self._dict)
                    return ret
        except Exception as e:
            print('ERROR: ')
            print(e)
