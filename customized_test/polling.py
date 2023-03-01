import os
import subprocess
import re
import time
import psutil

import uiautomator2

from lead_to_funtion import lead_to_function, launch_act
from tool import get_activity
import os


def get_monkey_pid():
    mon_pid = ''
    cmd = 'adb shell ps|grep monkey'
    temp_con = os.popen(cmd)
    temp_result = temp_con.readlines()[0].split(' ')
    for str in temp_result:
        if str != '' and str != 'shell':
            mon_pid = str
            break
    return mon_pid

def get_back_to_function(package_name, activity_name, search_action_list, mon_pid):
    # if get_activity.get_current_activity() in activity_name:
    #     return
    # # 这里记得自行设定规则
    # else:
    print("偏离功能入口")
    '''
    # 暂停monkey进程
    cmd = 'adb shell kill -STOP ' + mon_pid
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result)
    '''
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


def check(package_name, activity_name, search_action_list):
    while True:
        pass
    time.sleep(5)
    print("守护进程开始轮询")
    mon_pid = get_monkey_pid()
    while True:
        print("轮询ing")
        get_back_to_function(package_name, activity_name, search_action_list, mon_pid)
        time.sleep(10)


# check("gov.anzong.androidnga", "gov.anzong.androidnga.activity.SettingsActivity")
# print(get_current_activity())
if __name__ == '__main__':
    get_back_to_function("", "", "")
