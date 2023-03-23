import time
import os

import uiautomator2 as u2


def identify_function():
    # 连接设备
    device = u2.connect()
    devece2 = u2.connect()
    # 打印设备信息
    print(device.device_info)
    print(devece2.device_info)
    # dump layout文件
    print(type(device.dump_hierarchy()))
    # 字典，包含目前apk的包名和活动名
    apk_cur_info = device.app_current()
    print(apk_cur_info)

    # 点击坐标
    # device.click(838,183)

    # 点击content-desc
    # device.xpath("//*[@content-desc='搜索用户']").click()

#     x = device.window_size()[0]
#     y = device.window_size()[1]
#     device.swipe(x / 2, int(y / 1.2), x / 2, y / 6);
#
# identify_function()

################

# def drink():
#     for i in range(3):
#         print("111喝汤……")
#         time.sleep(1)
#     print("111结束")
#
#
#
# def eat():
#     while True:
#         print("222吃饭……")
#         print(os.getpid())
#         time.sleep(1)
#     print("222结束")
#
#
# if __name__ == '__main__':
#     # target:指定函数名
#     drink_process = multiprocessing.Process(target=drink)
#     drink_process.start()
#     eat_process = multiprocessing.Process(target=eat)
#     eat_process.start()
#     print("测试主进程是否工作")
#     print("主进程结束")
#     time.sleep(15)
#     print("吃的进程号： "+eat_process.pid.__str__())
#     eat_process.terminate()

# if __name__ == '__main__':
#     print("123")
#################
#
# import os
# import subprocess
# import re
#
# def get_event_device_path():
#     devices = os.popen("adb shell getevent -l").read()
#     pattern = re.compile(r"/dev/input/event\d")
#     event_devices = pattern.findall(devices)
#     if event_devices:
#         return event_devices[0]
#     return None
#
# def get_touch_events():
#     device_path = get_event_device_path()
#     if device_path:
#         cmd = "adb shell getevent -lt %s" % device_path
#         process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
#         while True:
#             output = process.stdout.readline().decode("utf-8")
#             if output == '' and process.poll() is not None:
#                 break
#             if "ABS_MT_POSITION_X" in output:
#                 x = output.split(" ")[-2].strip()
#                 y = process.stdout.readline().decode("utf-8").split(" ")[-2].strip()
#                 print("Touch event detected, x: %s, y: %s" % (x, y))
#

# def parse_IC3(file, pkg):
#     # 初始化文件目录
#     IC3_output_dir = "../result/" + pkg + "/IC3/IC3_output/"
#     results_parseIC3_dir = IC3_output_dir + 'parsed_ic3/'
#     if not os.path.exists(results_parseIC3_dir):
#         os.makedirs(results_parseIC3_dir)
#     IC3_atg = results_parseIC3_dir + pkg + '.txt'
#     with open(IC3_atg, 'w') as f:
#         f.write('')
#
#     # 原代码
#     dict = {}
#     if not os.path.exists(file):
#         return
#     f = open(file, 'r')
#     line = f.readline()
#     flag = -1
#     s = 0 # indicate component
#     brace = 0 # indicate the number of braces
#     while line:
#         if '{' in line:
#             brace += 1
#         if '}' in line:
#             brace -= 1
#         if 'components {' in line:
#             s = 1
#             flag = -1
#             tmp =''
#             brace = 1
#         elif s == 1 and 'name:' in line:
#             tmp = line.split(': "')[1].split('"')[0]
#             s = 2
#         elif s == 2 and 'kind: ACTIVITY' in line:
#             flag = 0
#             sourceActivity = tmp
#             s = 3
#         elif flag == 0 and "exit_points" in line:
#             flag = 1
#         elif flag == 1 and 'statement' in line:
#             stm = line.split(': "')[1].split('"')[0]
#             flag = 2
#         elif flag == 2 and 'method: "' in line:
#             mtd = line.split(': "<')[1].split('>"')[0]
#             flag = 3
#         elif flag == 3 and 'kind: ' in line:
#             if 'kind: ACTIVITY' in line:
#                 flag = 4
#             else:
#                 flag = 0
#         elif flag == 4 and 'kind: CLASS' in line:
#             flag = 5
#         elif flag == 5 and 'value' in line:
#             if ': "L' in line:
#                 targetActivity = line.strip().split(': "L')[1].split(';"')[0].replace('/', '.')
#                 if targetActivity.endswith('"'):
#                     targetActivity = targetActivity.split('"')[0]
#             else:
#                 targetActivity = line.strip().split(': "')[1].split(';"')[0].replace('/', '.')
#                 if targetActivity.endswith('"'):
#                     targetActivity = targetActivity.split('"')[0]
#             if not pkg in targetActivity:
#                 flag = 0
#                 continue
#             if not sourceActivity in dict.keys():
#                 dict[sourceActivity] = set()
#             dict[sourceActivity].add(targetActivity)
#             flag = 4
#         if brace == 1 and s == 3: # in component, find more exit_points
#             flag = 0
#         line = f.readline()
#
#     # 保存信息
#     for k, v in dict.items():
#         for v1 in v:
#             with open(IC3_atg, 'a') as f:
#                 f.write(k + '-->' + v1 + '\n')
#
#     return dict

if __name__ == "__main__":
    pass
    from androguard.misc import AnalyzeAPK
    from androguard.core.analysis.analysis import Analysis

    apk_path = "/home/xiaobudian/PycharmProjects/GraduationProject/crash_apk2/active-TAN-debug.apk"
    a, d, dx = AnalyzeAPK(apk_path)

    # 获取应用程序中所有类的列表
    classes = dx.get_classes()

    # 遍历所有类并获取方法调用图
    for clazz in classes:
        if 'activity' in clazz.name or 'Activity' in clazz.name:
            methods = clazz.get_methods()
            tempjudge = 0
            for method in methods:
                if 'activity' in method.name or 'Activity' in method.name:
                    tempjudge = 1
            if tempjudge == 0:
                continue
            elif tempjudge == 1:
                print("Class name:", clazz.name)
                for method in methods:
                    if 'activity' in method.name or 'Activity' in method.name:
                        print("    Method name:", method.name)
                        xref = method.get_xref_from()
                        for x in xref:
                            print("        Called from:", x)
        else:
            continue


