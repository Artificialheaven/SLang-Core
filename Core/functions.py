import configparser
import json
import os
import threading
import time
import uuid

import requests
import sqlite3

import Core.register
import Core.main

from Core.globals import global_var as global_dict

'''
@register.reg('', 1, '')
def name(parma: list, _dict: dict):
    pass
'''

register = Core.register.Router()


@register.reg('调试输出', 1, '控制台输出调试文本')
def debug_print(parma: list, _dict: dict):  # 所有的function都只有一个列表参数，接受文本传入的全部参数
    print(parma[0])


@register.reg('修改变量', 2, '修改SLang-Core全局变量')
def update_globals(parma: list, _dict: dict):
    global_dict[parma[0]] = parma[1]
    # Core.other.get_glo().add(parma[0], parma[1])


@register.reg('获取变量', 1, '获取SLang-Core全局变量')
def update_globals(parma: list, _dict: dict):
    # print(f'尝试获取全局变量{parma[0]}')
    # print(global_dict, _dict)
    return str(global_dict[parma[0]])


@register.reg('删除变量', 1, '删除SLang-Core全局变量')
def del_var(parma: list, _dict: dict):
    do_not_delete = ('debug')
    if parma[0] in do_not_delete:
        print('禁止删除SLang-Core核心全局变量')
    else:
        del global_dict[parma[0]]


@register.reg('赋值变量', 2, '赋值临时变量')
def set_room_var(parma: list, _dict: dict):
    _dict[parma[0]] = parma[1]


@register.reg('变量', 1, '获取临时变量')
def set_room_var(parma: list, _dict: dict):
    return str(_dict[parma[0]])


@register.reg('转全局变量', 2, '将本地变量赋值到全局变量')
def room_to_global(parma: list, _dict: dict):
    global_dict[parma[1]] = _dict[parma[0]]


@register.reg('cmd', 1, '运行一个shell命令')
def run_subshell(parma: list, _dict: dict):
    os.system(parma[0])


@register.reg('延迟', 1, '延迟n秒')
def name(parma: list, _dict: dict):
    time.sleep(int(parma[0]))


@register.reg('线程执行', 2, '线程执行一段Slang函数')
def thread_run_room(parma: list, _dict: dict):
    def run(text, d):
        from regs import register
        Slang = Core.main.Slang(register, d=d)
        Slang.run_room(text)

    threading.Thread(target=run, args=(parma[1], json.loads(parma[0])))


@register.reg('取出一行', 2, '取出特定文本的某一行')
def split_str_in_one(parma: list, _dict: dict):
    return parma[1].split('\n')[parma[0]]


@register.reg('删除一行', 2, '删除特定文本的某一行')
def delect_str_in_line(parma: list, _dict: dict):
    le = parma[1].split('\n')
    del le[parma[0] - 1]
    text = ''
    for i in range(len(le)):
        if i == len(le):
            text = text + le[i]
        else:
            text = text + le[i] + '\n'
    return text


@register.reg('取出行数', 2, '取出指定文本在来源的行数，失败返回-1 。如果省略最后一个参数，取出来源总行数')
def get_str_in_line(parma: list, _dict: dict):
    if len(parma) == 2:
        # 取出行数
        for i in parma[0].split('\n'):
            if parma[1] in i:
                return str(i)
    else:
        # 取出总行数
        return len(parma[0].split('\n'))


@register.reg('Json解析', 2, 'Json反序列化，并存入变量')
def json_loads(parma: list, _dict: dict):
    _dict[parma[0]] = json.loads(parma[1])


@register.reg('数组-取值', 3, '获取某一列表变量的某个值，并存入变量')
def get_list_value(parma: list, _dict: dict):
    _dict[parma[2]] = _dict[int(parma[0])][1]


@register.reg('字典-取值', 3, '获取某一字典变量中的某个值，并存入变量')
def get_dict_value(parma: list, _dict: dict):
    _dict[parma[2]] = _dict[parma[0]][parma[1]]


@register.reg('数组-取内容', 2, '获取某一列表变量的某个值，并返回')
def get_list_value(parma: list, _dict: dict):
    return str(_dict[parma[0]][int(parma[1])])


@register.reg('字典-取内容', 2, '获取某一字典变量中的某个值，并返回')
def get_dict_value(parma: list, _dict: dict):
    return str(_dict[parma[0]][parma[1]])


@register.reg('网页-访问', 3, '访问网页')
def request_web(parma: list, _dict: dict):
    if parma[1] == 'get':
        return requests.get(parma[0]).text
    else:
        return requests.post(parma[0], parma[2]).text


@register.reg('网页-下载', 3, '访问网页并将其下载到某一位置')
def request_web_download(parma: list, _dict: dict):
    content = bytes()
    if parma[1] == 'get':
        content = requests.get(parma[0]).content
    else:
        content = requests.post(parma[0], parma[2]).content
    f = open(parma[3], 'w')
    f.close()
    f = open(parma[3], 'rb+')
    f.write(content)
    f.close()


@register.reg('SQL-连接', 2, '执行连接SQLite数据库，并赋值给临时变量')
def connect_sqlite3(parma: list, _dict: dict):
    _dict[parma[1]] = sqlite3.connect(parma[0])


@register.reg('SQL-执行', 2, '使用变量中的sql执行sql语句')
def execute_sqlite3(parma: list, _dict: dict):
    cursor = _dict[parma[0]].cursor()
    cursor.execute(parma[1])
    cursor.commit()
    cursor.close()


@register.reg('SQL-读取', 3, '使用变量中的sql执行sql语句')
def execute_sqlite3(parma: list, _dict: dict):
    cursor = _dict[parma[0]].cursor()
    cursor.execute(parma[1])
    fatch = cursor.fetchall()
    _list = []
    for i in fatch:
        _list.append(i)
    _dict[parma[2]] = _list


@register.reg('现行时间戳', 0, '获取')
def run_with_system(parma: list, _dict: dict):
    return str(int(time.time()))


@register.reg('uuid', 0, '获取随机的uuid')
def get_uuid(parma: list, _dict: dict):
    return uuid.uuid1()


@register.reg('取反', 1, '若为真返回假，若为假，返回真')
def get_uuid(parma: list, _dict: dict):
    if parma[0] in ['True', 'true', '真', '1']:
        return '假'
    else:
        return '真'


@register.reg('读配置', 4, '读配置项')
def read_ini(parma: list, _dict: dict):
    config = configparser.ConfigParser()
    config.read(parma[0])
    try:
        return config.get(parma[1], parma[2], raw=parma[3])
    except Exception as e:
        print(f'读配置项异常：{e}')
        return parma[3]


@register.reg('写配置', 4, '写配置项')
def set_ini(parma: list, _dict: dict):
    f = open(parma[0], 'w+')
    config = configparser.ConfigParser()
    config.read(parma[0])
    if not config.has_section(parma[1]):
        config.add_section(parma[1])
    config[parma[1]][parma[2]] = parma[3]
    config.write(f)
    f.close()


@register.reg('计算', 1, '计算算式')
def execute_math(parma: list, _dict: dict):
    d, _d = {}, {}
    exec(f'''ret = {parma[0]}''', _d, d)
    return str(d['ret'])


@register.reg('置变量', 2, '将文本，字符串，列表，字典等填充进变量列表')
def set_var_pro(parma: list, _dict: dict):
    d, _d = {}, {}
    exec(f'''r = {parma[1]}''', _d, d)
    _dict[parma[0]] = d['r']


@register.reg('测试', 2, '运行一段Python代码。')
def execute_python(parma: list, _dict: dict):
    _d, d = {}, {}     # 站位
    exec(parma[1], _d, d)
    _dict[parma[0]] = d
