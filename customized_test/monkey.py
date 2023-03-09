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

    # 存储log的目录
    log_url_dir = os.path.abspath('..') + "/result/" + package_name + "/monkey/"
    file_list = os.listdir(log_url_dir)
    count = (len(file_list) + 1).__str__()
    # 本次monkey测试log的路径
    monkey_log_url = log_url_dir + "monkey_" + count + ".log"
    # 命令行命令cmd
    cmd = "adb shell monkey --throttle 50 -p " + package_name + " -v " + event_num.__str__() + " >" + monkey_log_url
    # 启动测试
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result)
    print("monkey测试结束")


# 分析monkey的log，后期可以添加其他分析方法
def monkey_log_analyse(package_name):
    log_url = "../result/" + package_name + "/monkey/"
    search_str = "Monkey aborted due to error"

    # 遍历目录中的所有文件
    import fnmatch
    for root, dirnames, filenames in os.walk(log_url):
        for filename in fnmatch.filter(filenames, '*'):
            # 打开文件，读取内容，并查找特定字符
            with open(os.path.join(root, filename), 'r') as file:
                contents = file.read()
                if search_str in contents:
                    print(f"{filename} 记录crash")
                    return True

    return False


if __name__ == '__main__':
    monkey_log_analyse("com.example.bottomnavigationactivity_menu")
