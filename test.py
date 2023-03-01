import os
import random
import multiprocessing
import subprocess
import sys

import uiautomator2 as u2
import time


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
if __name__ == "__main__":
    # get_touch_events()
    # device = u2.connect()
    # device.press("back")
    # result = subprocess.check_output(r"aapt dump badging ./input_apk_test/com.utazukin.ichaival_32.apk | grep launchable-activity | awk '{print $2}'", shell=True)
    # launch_activity = result.decode('utf-8').split('name=\'')[1].split('\'')[0]
    # print(launch_activity)

    # cmd = "adb shell am start -n " + "com.csnmedia.android.bg/.activities.MainActivity"
    # console_result = subprocess.check_output(cmd, shell=True)
    # print(console_result.decode("utf8"))
    import re

    s = "com.google.android.apps.chrome.Main.xml"
    s = re.sub(r'\d*\.xml$', '', s)
    print(s)
