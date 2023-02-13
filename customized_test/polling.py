import os
import subprocess
import re
import time
import psutil

import uiautomator2

from lead_to_funtion import lead_to_function, launch_act
from tool import get_activity
import os

def get_back_to_function(package_name, activity_name, search_action_list):
    # if get_activity.get_current_activity() in activity_name:
    #     return
    # # 这里记得自行设定规则
    # else:
    print("偏离功能入口")
    # 暂停monkey测试
    monkey_pid = os.getppid()
    monkey_proc = psutil.Process(monkey_pid)
    monkey_proc.suspend()
    # 返回功能入口
    print("尝试返回功能入口\n")
    lead_to_function(package_name, activity_name, search_action_list)
    # 恢复monkey测试
    monkey_proc.resume()
    print("已返回功能入口\n")



def check(package_name, activity_name, search_action_list):
    print("守护进程开始轮询")
    while True:
        time.sleep(10)
        print("轮询ing")
        get_back_to_function(package_name, activity_name, search_action_list)

# check("gov.anzong.androidnga", "gov.anzong.androidnga.activity.SettingsActivity")
# print(get_current_activity())
