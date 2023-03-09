import os
import subprocess
import re
import os
import time
import random
import psutil

import uiautomator2

from lead_to_funtion import lead_to_function, launch_act
from tool import get_activity


def get_monkey_pid():
    mon_pid = ''
    cmd = 'adb shell ps|grep monkey'
    temp_con = os.popen(cmd)
    temp_result = temp_con.readlines()[0].split(' ')
    for str in temp_result:
        if str != '' and str != 'shell' and str != 'root':
            mon_pid = str
            break
    return mon_pid

def get_back_to_function(package_name, activity_name, search_action_list, mon_pid):
    print("偏离功能入口")
    # 杀死monkey进程
    cmd = 'adb shell kill ' + mon_pid
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result)
    time.sleep(1)

    # 返回功能入口
    print("尝试返回功能入口\n")
    lead_to_function(package_name, activity_name, search_action_list)
    '''
    # 恢复monkey测试
    cmd = adb + ' shell kill -CONT ' + mon_pid
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result)
    '''
    time.sleep(1)
    print("已返回功能入口\n")


def get_func_activity_set(package_name, activity_name):
    static_atg_file = "../result/" + package_name + "/static_atg/static_atg.txt"
    # 功能包含活动划分界限
    with open(static_atg_file, 'r') as f:
        atg_lines = f.readlines()
    # 构建邻接表
    graph = {}  # graph表示有向图，字典类型
    for line in atg_lines:
        src, dst = line.split("-->")
        dst = dst.split("\n")[0]
        if src not in graph:
            graph[src] = set()
        if dst not in graph:
            graph[dst] = set()
        graph[src].add(dst)

    # 存储功能相关activity
    function_activity_set = set()
    def dfs(graph, node):
        function_activity_set.add(node)  # 标记节点为已访问
        for neighbor in graph.get(node, set()):  # 遍历该节点的所有邻居节点
            if neighbor not in function_activity_set:  # 如果邻居节点还没有访问过，就递归调用DFS
                dfs(graph, neighbor)
    dfs(graph, activity_name)

    # 去除直接导向入口activity的活动
    stop_activity_set = set()
    for line in atg_lines:
        src, dst = line.split("-->")
        dst = dst.split("\n")[0]
        if dst == activity_name:
            stop_activity_set.add(src)
    return function_activity_set, stop_activity_set


def check(apk_path, package_name, activity_name, search_action_list, func_act):
    # while True:
    #     pass
    time.sleep(3)
    print("守护进程开始轮询")
    mon_pid = get_monkey_pid()
    print("monkey_id:", mon_pid)
    function_activity_set, stop_activity_set = get_func_activity_set(package_name, func_act)
    print("功能包含的活动：", function_activity_set - stop_activity_set)
    print("轮询ing")
    # cmd = 'adb shell kill -STOP ' + mon_pid
    # print(cmd)
    # console_result = subprocess.check_output(cmd, shell=True)
    # print(console_result)
    current_activity = get_activity.get_current_activity()
    current_package = get_activity.get_current_package()
    print("current_activity: ", current_activity)
    print("功能活动：", func_act)
    if any(current_activity in act for act in function_activity_set - stop_activity_set) or current_activity == func_act or current_activity in func_act:
        # cmd = 'adb shell kill -CONT ' + mon_pid
        # console_result = subprocess.check_output(cmd, shell=True)
        # print(console_result)
        print("当前活动属于功能")
        return True, mon_pid
    elif current_activity in stop_activity_set or current_package != package_name:
        # cmd = 'adb shell kill -CONT ' + mon_pid
        # console_result = subprocess.check_output(cmd, shell=True)
        # print(console_result)
        # 这里要马上终止monkey
        print("当前活动偏离功能")
        return False, mon_pid
    else:
        # 这里要概率终止monkey
        if random.random() < 0.2:
            # cmd = 'adb shell kill -CONT ' + mon_pid
            # console_result = subprocess.check_output(cmd, shell=True)
            # print(console_result)
            print("未知act, return")
            return False, mon_pid
        else:
            # cmd = 'adb shell kill -CONT ' + mon_pid
            # console_result = subprocess.check_output(cmd, shell=True)
            # print(console_result)
            print("未知act, continue")
            return True, mon_pid

        # cmd = 'adb shell kill -CONT ' + mon_pid
        # console_result = subprocess.check_output(cmd, shell=True)
        # print(console_result)
        # # get_back_to_function(package_name, activity_name, search_action_list, mon_pid)
        # time.sleep(1)


# check("gov.anzong.androidnga", "gov.anzong.androidnga.activity.SettingsActivity")
# print(get_current_activity())
if __name__ == '__main__':
    # get_back_to_function("", "", "")
    function_activity_set, stop_activity_set = get_func_activity_set("rodrigodavy.com.github.pixelartist", "rodrigodavy.com.github.pixelartist.MainActivity")
    print(function_activity_set)
    print(stop_activity_set)
