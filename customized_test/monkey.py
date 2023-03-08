import os
import subprocess
import multiprocessing
import polling
import random


# 开启monkey测试
def monkey_test(apk_path, package_name, activity_name, search_action_list):
    # 先启动守护进程轮询
    # polling_process = multiprocessing.Process(target=polling.check, args=(apk_path, package_name, activity_name, search_action_list))
    # polling_process.daemon = True
    # polling_process.start()

    # monkey模拟活动数
    event_num = 10000
    # log的url，如果目录不存在则创建
    log_url = os.path.abspath('..') + "/result/" + package_name
    if not os.path.exists(log_url):
        os.makedirs(log_url)
    # 命令行命令cmd
    cmd = "adb shell monkey --throttle 50 -p " + package_name + " -v " + event_num.__str__() + " >" + log_url + "/monkey" + random.randint(1, 10000).__str__() + ".log"
    # 启动测试
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result)
    print("monkey测试结束")
