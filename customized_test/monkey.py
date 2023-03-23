import os
import subprocess


# 开启monkey测试
def monkey_test(apk_path, package_name, activity_name, search_action_list):
    cmd = "adb shell wm overscan 0,-140,0,-150"
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result)
    print("禁止上下边栏")
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
    arguments = "--throttle 200 --pct-touch 42 --pct-motion 8 --pct-trackball 2 --pct-nav 0 --pct-majornav 0 --pct-syskeys 0 --pct-appswitch 25 --pct-flip 15 --pct-anyevent 2 --pct-pinchzoom 6"
    package_args = " -p " + package_name
    cmd = "adb shell monkey " + arguments + package_args + " -v " + event_num.__str__() + " >" + monkey_log_url
    # 启动测试
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result)
    print("monkey测试结束")


# 分析monkey的log，后期可以添加其他分析方法
def monkey_log_analyse(package_name):
    log_url = "../result/" + package_name + "/monkey/"
    search_str = "Monkey aborted due to error"
    search_str2 = "Events injected:"

    # 遍历目录中的所有文件
    import fnmatch
    for root, dirnames, filenames in os.walk(log_url):
        for filename in fnmatch.filter(filenames, '*'):
            # 打开文件，读取内容，并查找特定字符
            with open(os.path.join(root, filename), 'r') as file:
                contents = file.read()
                if search_str in contents or search_str2 in contents:
                    print(f"{filename} 记录crash")
                    return True

    return False


def monkey_test2(package_name):
    cmd = "adb shell wm overscan 0,-140,0,0"
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result)
    print("禁止上边栏")
    # monkey模拟活动数
    event_num = 100000

    # 存储log的目录
    log_url_dir = os.path.abspath('..') + "/result/" + package_name + "/monkey/"
    if not os.path.exists(log_url_dir):
        os.mkdir(log_url_dir)
    file_list = os.listdir(log_url_dir)
    count = (len(file_list) + 1).__str__()
    # 本次monkey测试log的路径
    monkey_log_url = log_url_dir + "monkey_" + count + ".log"
    # 命令行命令cmd
    arguments = ""
    arguments = "--throttle 200 --pct-touch 42 --pct-motion 8 --pct-trackball 2 --pct-nav 0 --pct-majornav 0 --pct-syskeys 0 --pct-appswitch 25 --pct-flip 15 --pct-anyevent 2 --pct-pinchzoom 6"
    package_args = " -p " + package_name
    cmd = "adb shell monkey " + arguments + package_args + " -v " + event_num.__str__() + " >" + monkey_log_url
    # 启动测试
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result)
    print("monkey测试结束")


if __name__ == '__main__':
    monkey_log_analyse("d.d.meshenger")
