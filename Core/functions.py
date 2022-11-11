import json
import os
import threading
import time
import requests
import sqlite3

import Core.other
import Core.main


'''
@Core.other.get_reg().reg('', 1, '')
def name(parma: list, _dict: dict):
    pass
'''


@Core.other.get_reg().reg('调试输出', 1, '控制台输出调试文本')
def debug_print(parma: list, _dict: dict):  # 所有的function都只有一个列表参数，接受文本传入的全部参数
    print(parma[0])


@Core.other.get_reg().reg('修改变量', 2, '修改SLang-Core全局变量')
def update_globals(parma: list, _dict: dict):
    Core.other.get_glo().add(parma[0], parma[1])


@Core.other.get_reg().reg('获取变量', 1, '获取SLang-Core全局变量')
def update_globals(parma: list, _dict: dict):
    # print(f'尝试获取全局变量{parma[0]}')
    return str(Core.other.get_glo().get(parma[0]))


@Core.other.get_reg().reg('删除变量', 1, '删除SLang-Core全局变量')
def del_var(parma: list, _dict: dict):
    do_not_delete = ('debug')
    if parma[0] in do_not_delete:
        print('禁止删除SLang-Core核心全局变量')
    else:
        del Core.other.get_glo()()[parma[0]]


@Core.other.get_reg().reg('赋值变量', 2, '赋值临时变量')
def set_room_var(parma: list, _dict: dict):
    _dict[parma[0]] = parma[1]


@Core.other.get_reg().reg('变量', 1, '获取临时变量')
def set_room_var(parma: list, _dict: dict):
    return str(_dict[parma[0]])


@Core.other.get_reg().reg('转全局变量', 2, '将本地变量赋值到全局变量')
def room_to_global(parma: list, _dict: dict):
    Core.other.get_glo()()[parma[1]] = _dict[parma[0]]


@Core.other.get_reg().reg('cmd', 1, '运行一个shell命令')
def run_subshell(parma: list, _dict: dict):
    os.system(parma[0])


@Core.other.get_reg().reg('延迟', 1, '延迟n秒')
def name(parma:list, _dict: dict):
    time.sleep(int(parma[0]))


@Core.other.get_reg().reg('线程执行', 2, '线程执行一段Slang函数')
def thread_run_room(parma:list, _dict: dict):
    def run(text, d):
        Slang = Core.main.Slang(d=d)
        Slang.run_room(text)
    threading.Thread(target=run, args=(parma[1], json.loads(parma[0])))


@Core.other.get_reg().reg('取出一行', 2, '取出特定文本的某一行')
def split_str_in_one(parma:list, _dict: dict):
    return parma[1].split('\n')[parma[0]]


@Core.other.get_reg().reg('删除一行', 2, '删除特定文本的某一行')
def delect_str_in_line(parma:list, _dict: dict):
    le = parma[1].split('\n')
    del le[parma[0]-1]
    text = ''
    for i in range(len(le)):
        if i == len(le):
            text = text + le[i]
        else:
            text = text + le[i] + '\n'
    return text


@Core.other.get_reg().reg('取出行数', 2, '取出指定文本在来源的行数，失败返回-1 。如果省略最后一个参数，取出来源总行数')
def get_str_in_line(parma: list, _dict: dict):
    if len(parma) == 2:
        # 取出行数
        for i in parma[0].split('\n'):
            if parma[1] in i:
                return str(i)
    else:
        # 取出总行数
        return len(parma[0].split('\n'))


@Core.other.get_reg().reg('Json解析', 2, 'Json反序列化，并存入变量')
def json_loads(parma: list, _dict: dict):
    _dict[parma[0]] = json.loads(parma[1])


@Core.other.get_reg().reg('数组取值', 3, '获取某一列表变量的某个值，并存入变量')
def get_list_value(parma: list, _dict: dict):
    _dict[parma[2]] = _dict[parma[0]][1]


@Core.other.get_reg().reg('字典取值', 3, '获取某一字典变量中的某个值，并存入变量')
def get_dict_value(parma: list, _dict: dict):
    _dict[parma[2]] = _dict[parma[0]][parma[1]]


@Core.other.get_reg().reg('网页-访问', 4, '访问网页')
def request_web(parma: list, _dict: dict):
    if parma[1] == 'get':
        return requests.get(parma[0], cookies=parma[3]).text
    else:
        return requests.post(parma[0], parma[2], cookies=parma[3]).text


@Core.other.get_reg().reg('网页-下载', 4, '访问网页并将其下载到某一位置')
def request_web_download(parma: list, _dict: dict):
    content = bytes()
    if parma[1] == 'get':
        content = requests.get(parma[0]).content
    else:
        content = requests.post(parma[0], parma[2]).content
    f = open(parma[3], 'rb+')
    f.write(content)
    f.close()


@Core.other.get_reg().reg('SQL-连接', 2, '执行连接SQLite数据库，并赋值给临时变量')
def connect_sqlite3(parma: list, _dict: dict):
    _dict[parma[1]] = sqlite3.connect(parma[0])


@Core.other.get_reg().reg('SQL-执行', 2, '使用变量中的sql执行sql语句')
def execute_sqlite3(parma: list, _dict: dict):
    cursor = _dict[parma[0]].cursor()
    cursor.execute(parma[1])
    cursor.commit()
    cursor.close()


@Core.other.get_reg().reg('SQL-读取', 3, '使用变量中的sql执行sql语句')
def execute_sqlite3(parma: list, _dict: dict):
    cursor = _dict[parma[0]].cursor()
    cursor.execute(parma[1])
    fatch = cursor.fetchall()
    _list = []
    for i in fatch:
        _list.append(i)

