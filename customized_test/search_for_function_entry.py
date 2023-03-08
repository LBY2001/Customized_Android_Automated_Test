import subprocess
import os
import time

import numpy as np
import xml.etree.ElementTree as et
import uiautomator2 as u2

import lead_to_funtion
from tool import eigenvector
from tool import get_activity


# 遍历xml文件，返回所有可以点击的按钮的list
def traversal(rootNode, level):
    clickable_list = []
    # clickable=true,则将et对象转化为string后入队
    if 'clickable' in rootNode.attrib and rootNode.attrib['clickable'] == 'true':
        clickable_list.append(et.tostring(rootNode, encoding='unicode').split('\n')[0])
    # 递归子节点实现遍历
    childrenNode = list(rootNode)
    # 递归出口
    if len(childrenNode) == 0:
        return clickable_list
    # 递归
    for child in childrenNode:
        clickable_list = clickable_list + traversal(child, level + 1)
    return clickable_list


# xml字符串转化为可执行的代码，通过坐标点击
def uicode2pythoncode(clickable_widget):
    bounds = clickable_widget.split("bounds=\"[")[1]
    x = int(bounds.split(',')[0]) + 1
    y = int(bounds.split(',')[1].split(']')[0]) + 1
    return 'device.click(' + x.__str__() + ', ' + y.__str__() + ')'


# 取出当前页面的所有action，以便后续入队
def analyse_ui():
    # 获取当前页面的layout文件，存入tempXml临时文件
    # 连接设备
    device = u2.connect()
    # 打印设备信息
    print(device.device_info)
    # dump当前页面
    layout_code = device.dump_hierarchy()
    tempXml = '../tempFile/tempXml.xml'
    with open(tempXml, 'w', encoding='UTF-8') as f:
        f.write(layout_code)

    # 取页面所有clickable=True控件的入栈
    tree = et.ElementTree(file=tempXml)
    root = tree.getroot()
    clickable_list = traversal(root, 1)
    print("可点击控件的总数量：", len(clickable_list))
    for _ in clickable_list:
        print(_)

    # 转换为uiautomator代码
    code = []
    for clickable_widget in clickable_list:
        code.append(uicode2pythoncode(clickable_widget))
    print("uicode:", code)

    return code, clickable_list


# 返回是否找到功能以及点击的命令
def find_function(function_dict):
    func_name = function_dict['function_name']
    widget = function_dict['widget']
    ui_hash = function_dict['ui_hash']
    package_name = function_dict['package']

    # 如果当前页面的hash对上了
    # hash对上了但是可能还是缺功能，因为判断hash的代码有漏洞，详情见2023-03-01笔记
    # 因此需要再判断一下widget是否在xml文件中
    device = u2.connect()
    layout_code = device.dump_hierarchy()
    tempXml = '../tempFile/tempXml3.xml'
    with open(tempXml, 'w', encoding='UTF-8') as f:
        f.write(layout_code)
    if eigenvector.get_vector('../tempFile/tempXml3.xml', package_name) == ui_hash:
        if widget in layout_code:
            x = widget.split('bounds=\"[')[1].split(',')[0]
            y = widget.split('bounds=\"[' + x + ',')[1].split(']')[0]
            x = (int(x) + 1).__str__()
            y = (int(y) + 1).__str__()
            return True, 'device.click(' + x + ',' + y + ')'

    # 页面不一样但是找到功能
    # 方法是尝试点击该语义的按钮，但是定位时间太长，所以先判断以下页面里面是否包含这个语义字段
    if func_name in layout_code:
        try:
            str = 'device(text=\'' + func_name + '\').click()'
            exec(str)
            return True, str
        except:
            try:
                str = 'device.xpath("//*[@content-desc=\'' + func_name + '\']").click()'
                exec(str)
                return True, str
            except:
                return False, ''
    return False, ''


def update_ui(package_name, activity_name, ui_hash):
    # 连接设备
    device = u2.connect()
    # 打印设备信息
    print(device.device_info)

    # activity变化了不算作页面变换，返回False
    if get_activity.get_current_activity() != activity_name:
        return False

    # dump当前页面
    layout_code = device.dump_hierarchy()
    tempXml = '../tempFile/tempXml2.xml'
    with open(tempXml, 'w', encoding='UTF-8') as f:
        f.write(layout_code)

    if eigenvector.get_vector('../tempFile/tempXml2.xml', package_name) in ui_hash:
        return False
    else:
        return True


def search(package_name, activity_name, function_name):
    # 判断是否记录过该功能
    list_url = '../result/' + package_name + '/' + package_name + '.npy'
    temp_list = np.load(list_url, allow_pickle=True).tolist()
    has_been_recorded = False   # 标记是否记录该功能
    function_dict = {}
    for temp_dict in temp_list:
        if temp_dict['function_name'] == function_name:
            has_been_recorded = True
            function_dict = temp_dict
    if not has_been_recorded:
        return ["This function has not been recorded."]

    # 初始化变量
    entry_action = []  # 到达分析入口的action  eg.["","","",...]
    action = []        # 配合entry_action，一起执行的action  eg[""]
    total_action = []  # 把entry_action和action存在一起，等待入队  eg[["","",""],[""]]
    total_action_list = []   # 待执行action队   [[["","",""],[""]],[["","",""],[""]],...]

    # 先到探索到目前的入口
    print("跳转到初始activity")
    lead_to_funtion.launch_act(package_name, activity_name)
    time.sleep(0.5)
    # 循环执行队中的信息
    total_action_list.append([[""],[""]])
    judge_action = ["如果队里面的页面入口相同，提取页面一次就好，通过这个变量判断"]
    ui_hash = []
    action = analyse_ui()[0]
    while len(total_action_list) != 0:
        # 等待执行的entry和action
        temp = total_action_list.pop(0)
        exec_entryaction = temp[0]
        exec_action = temp[1]
        # 分析当前页面信息，提取action，入队
        action = [""]
        entry_action = [""]
        '''
        time.sleep(0.7)
        action = analyse_ui()[0]
        if judge_action != exec_entryaction:
            judge_action = exec_entryaction
            for _ in action:
                total_action = [entry_action, [_]]
                total_action_list.append(total_action)
        '''
        # 先执行entry_action到达action入口，再执行action
        lead_to_funtion.to_entry(exec_entryaction, package_name, activity_name)
        time.sleep(0.5)
        print("\n点击前页面分析：")
        action = analyse_ui()[0]
        lead_to_funtion.perform_the_action(exec_action)
        # 分析是否包含目标功能
        judge, action_temp = find_function(function_dict)
        if judge:
            # print(exec_entryaction + exec_action, action_temp)
            # x = function_dict['widget'].split('bounds=\"[')[1].split(',')[0]
            # y = function_dict['widget'].split('bounds=\"[' + x + ',')[1].split(']')[0]
            # x = (int(x) + 1).__str__()
            # y = (int(y) + 1).__str__()
            temp_list = exec_entryaction + exec_action
            temp_list.append(action_temp)
            print("找到功能入口")
            print("到达功能入口操作：", temp_list)
            return temp_list
        # 分析点击后页面是否变化
        if update_ui(package_name, activity_name, ui_hash) or temp == [[""], [""]]:
            ui_hash.append(eigenvector.get_vector('../tempFile/tempXml2.xml', package_name))
            entry_action = exec_entryaction + exec_action
            time.sleep(0.7)
            print("\n点击后页面分析：")
            action = analyse_ui()[0]
            for _ in action:
                total_action = [entry_action, [_]]
                total_action_list.append(total_action)
            # 分析下拉后页面是否变化
            swip_list = []
            while True:
                # 下拉页面
                device = u2.connect()
                x = device.window_size()[0]
                y = device.window_size()[1]
                device.swipe(x / 2, int(y / 1.2), x / 2, y / 6)
                swip_list.append("device.swipe(" + x.__str__() +" / 2, int(" + y.__str__() + " / 1.2), " + x.__str__() + " / 2, " + y.__str__() + " / 6)")
                # 判断下拉后是否包含功能
                judge, action_temp = find_function(function_dict)
                if judge:
                    temp_list = exec_entryaction + exec_action
                    for swip in swip_list:
                        temp_list.append(swip)
                    temp_list.append(action_temp)
                    print("找到功能入口")
                    print("到达功能入口操作：", temp_list)
                    return temp_list
                # 下拉后没有页面的更新就结束，否则更新队列
                if update_ui(package_name, activity_name, ui_hash):
                    ui_hash.append(eigenvector.get_vector('../tempFile/tempXml2.xml', package_name))
                    entry_action = exec_entryaction + exec_action
                    for swip in swip_list:
                        entry_action.append(swip)
                    time.sleep(0.7)
                    print("\n下拉后页面分析：")
                    action = analyse_ui()[0]
                    for _ in action:
                        total_action = [entry_action, [_]]
                        total_action_list.append(total_action)
                else:
                    break


if __name__ == '__main__':
    search_list = search("gov.anzong.androidnga", "gov.anzong.androidnga.activity.SettingsActivity", "黑名单")

