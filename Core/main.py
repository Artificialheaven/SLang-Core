# Core运行器
import Core.other


class Slang:
    _dict = {}

    def __init__(self, d={}):
        self._dict = d
        # 创建初始变量表

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
        for i in Core.other.get_reg()():
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
                    if text[count:count+3] == '>=<' and do:
                        if dst == 0:
                            _list.append(text[len('【' + i):count])
                            # print('定位到第一个参数' + text[len('【' + i):count])
                        else:
                            _list.append(text[dst:count])
                            # print('定位到位于中部的参数' + text[dst:count])
                        dst = count + 3  # dst为定位前端
                    if len(_list) == 0 and count == len(text)-1:
                        # 无参数的或者只有一个的
                        if not text == '【' + i + '】':
                            # 包含一个参数，把去掉首尾的【函数】去掉剩下的都是参数
                            _list.append(text[len('【' + i):len(text)-1])
                            # print('定位到唯一参数' + text[len('【' + i):len(text)-1])
                    if not dst == 0 and do and text[count] == '】' and count == len(text)-1:
                        _list.append(text[dst:len(text)-1])
                        # print('定位到末尾参数' + text[dst:len(text)-1])
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
                ret = Core.other.get_reg().call(i, _list, self._dict)
                return ret
