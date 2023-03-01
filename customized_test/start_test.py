import os
import subprocess
import multiprocessing
import time
import numpy as np

import tool.get_activity
from lead_to_funtion import lead_to_function, launch_app, launch_act
import monkey
import polling
from search_for_function_entry import search


def get_activity_name(package_name, function_name):
    # 判断是否记录过该功能
    list_url = '../result/' + package_name + '/' + package_name + '.npy'
    temp_list = np.load(list_url, allow_pickle=True).tolist()
    has_been_recorded = False  # 标记是否记录该功能
    for temp_dict in temp_list:
        if temp_dict['function_name'] == function_name:
            has_been_recorded = True
            return temp_dict['activity']
    if not has_been_recorded:
        return "This function has not been recorded."


def run_test(apk_url, function_name):
    package_name = tool.get_activity.get_package_name(apk_url)
    # 通过之前存储的npy文件获得activity
    activity_name = get_activity_name(package_name, function_name)
    # 先启动app，防止不能直接启动活动
    launch_app(apk_url, package_name, activity_name)
    # 先启动到功能模块活动
    # launch_act(package_name, activity_name)
    # 寻找功能模块入口
    search_result_list = search(package_name, activity_name, function_name)
    if not search_result_list:
        print("Can‘t find the function.")
        return
    if search_result_list[0] == "This function has not been recorded.":
        print("This function has not been recorded.")
        return
    time.sleep(5)
    # 导向功能入口
    lead_to_function(package_name, activity_name, search_result_list)

    # 新建monkey测试进程
    monkey_process = multiprocessing.Process(target=monkey.monkey_test, args=(package_name, activity_name, search_result_list))
    monkey_process.start()
    while monkey_process.is_alive():
        pass

if __name__ == '__main__':
    run_test("../input_apk_test/com.utazukin.ichaival_32.apk", "Settings")
    # run_test("com.example.bottomnavigationactivity_menu", "DIALOG")
