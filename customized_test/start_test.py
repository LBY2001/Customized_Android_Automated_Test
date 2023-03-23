import multiprocessing
import os
import time
import sys

import numpy as np


import monkey
import polling
import tool.get_activity
import repkg_apk.repkg
from lead_to_funtion import lead_to_function, launch_app
from search_for_function_entry import search
from static_analysis import get_at, ic3_analyse, soot_analyse


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


def get_static_atg(package_name, apk_url):
    # 静态分析生成atg
    # if not os.path.exists("../result/" + package_name + "/static_atg/"):
    #     os.chdir("../static_analysis")
    #     soot_analyse.get_soot_output(apk_url)
    #     soot_analyse.get_soot_atg(apk_url)
    #     ic3_analyse.get_ic3_output(apk_url)
    #     get_at.get_at(apk_url)
    #     os.chdir("../customized_test")

    # 多进程静态分析生成atg
    if not os.path.exists("../result/" + package_name + "/static_atg/"):
        os.chdir("../static_analysis")
        soot_analyse.get_soot_output(apk_url)
        # soot_atg进程
        soot_atg_process = multiprocessing.Process(target=soot_analyse.get_soot_atg, args=(apk_url,))
        print("========soot atg进程开启==========")
        soot_atg_process.start()
        # ic3进程
        ic3_process = multiprocessing.Process(target=ic3_analyse.get_ic3_output, args=(apk_url,))
        print("========ic3 atg进程开启==========")
        ic3_process.start()
        # 进程结束再继续
        soot_atg_process.join()
        ic3_process.join()
        print("多进程结束")
        # 运行 get_at
        get_at.get_at(apk_url)
        os.chdir("../customized_test")


def run_test(apk_url, function_name):
    package_name = tool.get_activity.get_package_name(apk_url)
    # 通过之前存储的npy文件获得activity
    activity_name = get_activity_name(package_name, function_name)

    # repkg apk，以防singleTask重置monkey测试
    temp_judge, temp_url = repkg_apk.repkg.repackage(apk_url)
    apk_url = temp_url
    if temp_judge:
        print("apk存在singleTask，重打包成功")
    else:
        print("apk无需重新打包，或重新打包失败")

    # 先启动app，防止不能直接启动活动
    launch_app(apk_url, package_name, activity_name)
    # 先启动到功能模块活动
    # launch_act(package_name, activity_name)
    # 若功能名为空，则是手动无法找到功能入口，直接启动monkey测试
    if function_name == '':
        print("直接启动monkey测试")
        monkey.monkey_test(apk_url, package_name, '', [])
    # 寻找功能模块入口
    search_result_list = search(package_name, activity_name, function_name)
    if not search_result_list:
        print("Can‘t find the function.")
        return
    if search_result_list[0] == "This function has not been recorded.":
        print("This function has not been recorded.")
        return
    time.sleep(3)
    # 导向功能入口
    lead_to_function(package_name, activity_name, search_result_list)

    # 静态分析生成atg
    get_static_atg(package_name, apk_url)

    # 换一个活动开始判断测试是否跳出功能
    func_act = tool.get_activity.get_current_activity()
    current_package = tool.get_activity.get_current_package()
    if current_package != package_name:
        print("crash：功能入口跳出app，终止测试")
        return

    # monkey测试log的url，如果目录不存在则创建
    log_url = "../result/" + package_name + "/monkey/"
    if not os.path.exists(log_url):
        os.makedirs(log_url)
    # 新建monkey测试进程
    monkey_process = multiprocessing.Process(target=monkey.monkey_test, args=(apk_url, package_name, activity_name, search_result_list))
    monkey_process.start()
    while True:
        time.sleep(4)
        if monkey_process.is_alive():
            try:
                tag, mon_pid = polling.check(apk_url, package_name, activity_name, search_result_list, func_act)
            except:
                if monkey.monkey_log_analyse(package_name):
                    print("发现crash")
                ########### 要记得清空log
                return
            if mon_pid == "-1":
                if monkey.monkey_log_analyse(package_name):
                    print("发现crash")
                ########### 要记得清空log
                return
            if tag:
                continue
            else:
                monkey_process.terminate()
                polling.get_back_to_function(package_name, activity_name, search_result_list, mon_pid)
        if not monkey_process.is_alive():
            if monkey.monkey_log_analyse(package_name):
                print("发现crash")
                ########### 要记得清空log
                return
            monkey_process = multiprocessing.Process(target=monkey.monkey_test, args=(apk_url, package_name, activity_name, search_result_list))
            monkey_process.start()

    if monkey.monkey_log_analyse(package_name):
        print("发现crash")
        ########### 要记得清空log
        return


def tool_compare():
    pass
    # time1 = time.time()
    # run_test("../input_apk_test/d.d.meshenger.apk", "About")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('d.d.meshenger.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)
    #
    # time1 = time.time()
    # run_test("../input_apk_test/ShaderEditor.apk", "Load sample")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('ShaderEditor.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)

    # time1 = time.time()
    # run_test("../input_apk_test/Fedilab.apk", "Proxy")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('Fedilab.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)

    # time1 = time.time()
    # run_test("../input_apk_test/Simple-Gallery-master.apk", "Settings")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('Simple-Gallery-master.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)
    #
    # time1 = time.time()
    # run_test("../input_apk_test/openhab-android.apk", "Settings")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('openhab-android.apk: ' + (time.time() - time1).__str__() + '\n')

    #=========== crash_apk2=============

    # time1 = time.time()
    # run_test("../crash_apk2/active-TAN-debug.apk", "Manual")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('active-TAN-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)
    #
    # time1 = time.time()
    # run_test("../crash_apk2/calendar-core-debug.apk", "Settings")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('calendar-core-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)
    #
    # time1 = time.time()
    # run_test("../crash_apk2/omweather-master.apk", "Settings")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('omweather-master.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)

    # time1 = time.time()
    # run_test("../crash_apk2/org.unifiedpush.distributor.nextpush.apk", "")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('org.unifiedpush.distributor.nextpush.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)

    # time1 = time.time()
    # run_test("../crash_apk2/paintroid-debug.apk", "Load image")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('paintroid-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)

    # time1 = time.time()
    # run_test("../crash_apk2/TorrServe_MatriX.120.Client-debug.apk", "")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('TorrServe_MatriX.120.Client-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)
    #
    # time1 = time.time()
    # run_test("../crash_apk2/uaTranslit-master.apk", "")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('uaTranslit-master.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)

    # time1 = time.time()
    # run_test("../crash_apk2/Xtra-master.apk", "Following")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('Xtra-master.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)

    # time1 = time.time()
    # run_test("../crash_apk2/YourLocalWeather-debug.apk", "Settings")
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'a') as f:
    #     f.write('YourLocalWeather-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    # time.sleep(30)


def monkey_compare():
    pass
    # time1 = time.time()
    # apkurl = "../input_apk_test/d.d.meshenger.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('d.d.meshenger.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(20)
    #
    # time1 = time.time()
    # apkurl = "../input_apk_test/ShaderEditor.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('ShaderEditor.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(20)
    #
    # time1 = time.time()
    # apkurl = "../input_apk_test/Fedilab.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('Fedilab.apk ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(20)

    # time1 = time.time()
    # apkurl = "../input_apk_test/Simple-Gallery-master.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('Simple-Gallery-master.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)

    # time1 = time.time()
    # apkurl = "../input_apk_test/openhab-android.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('openhab-android.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)

    # =========== crash_apk2

    # time1 = time.time()
    # apkurl = "../crash_apk2/active-TAN-debug.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('active-TAN-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)
    #
    # time1 = time.time()
    # apkurl = "../crash_apk2//calendar-core-debug.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('calendar-core-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)
    #
    # time1 = time.time()
    # apkurl = "../crash_apk2//omweather-master.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('omweather-master.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)
    #
    # time1 = time.time()
    # apkurl = "../crash_apk2//org.unifiedpush.distributor.nextpush.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('org.unifiedpush.distributor.nextpush.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)

    # time1 = time.time()
    # apkurl = "../crash_apk2//paintroid-debug.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('paintroid-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)
    #
    # time1 = time.time()
    # apkurl = "../crash_apk2//TorrServe_MatriX.120.Client-debug.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('TorrServe_MatriX.120.Client-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)
    #
    # time1 = time.time()
    # apkurl = "../crash_apk2//uaTranslit-master.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('uaTranslit-master.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)
    #
    # time1 = time.time()
    # apkurl = "../crash_apk2//Xtra-master.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('Xtra-master.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)
    #
    # time1 = time.time()
    # apkurl = "../crash_apk2//YourLocalWeather-debug.apk"
    # pkg = tool.get_activity.get_package_name(apkurl)
    # try:
    #     monkey.monkey_test2(package_name=pkg)
    # except:
    #     with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'a') as f:
    #         f.write('YourLocalWeather-debug.apk: ' + (time.time() - time1).__str__() + '\n')
    #         time.sleep(30)


if __name__ == '__main__':

    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/crash_Log", 'w') as f:
    #     f.write('')
    # with open("/home/xiaobudian/PycharmProjects/GraduationProject/monkey_Log", 'w') as f:
    #     f.write('')
    tool_compare()
    monkey_compare()
    time2 = time.time()
    url = '/home/xiaobudian/PycharmProjects/GraduationProject/crash_apk2/paintroid-debug.apk'
    pkg = tool.get_activity.get_package_name(url)
    print(pkg)
    get_static_atg(pkg, url)
    print("使用多线程耗费时间: ", time.time() - time2)
