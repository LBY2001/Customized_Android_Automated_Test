import subprocess
import os
import time

import uiautomator2 as u2


def launch_app(package_name, activity_name):
    print("启动" + package_name)
    adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
    if package_name not in activity_name:
        activity_name = package_name + activity_name
    cmd = adb + " shell am start -n " + package_name + '/' + activity_name.split(package_name)[1].replace(activity_name.split(package_name)[1].split('.')[-1], 'MainActivity')
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result.decode("utf8"))


def launch_act(package_name, activity_name):
    # 这里如果activity正确但是fragment不对就不会变，所以需要重新启动activity哦
    pass
    # Main不能冷启动
    if 'MainActivity' not in activity_name:
        print("启动" + package_name)
        adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
        if package_name not in activity_name:
            activity_name = package_name + activity_name
        # 先关闭app
        cmd = adb + " shell am force-stop " + package_name
        console_result = subprocess.check_output(cmd, shell=True)
        print(console_result.decode("utf8"))
        time.sleep(2)
        # 再冷启动活动
        cmd = adb + " shell am start -n " + package_name + '/' + activity_name.split(package_name)[1]
        console_result = subprocess.check_output(cmd, shell=True)
        print(console_result.decode("utf8"))
    else:
        # 启动Main
        adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
        cmd = adb + " shell am start -n " + package_name + '/' + activity_name.replace(package_name, '')
        console_result = subprocess.check_output(cmd, shell=True)
        time.sleep(1)
        print(console_result.decode("utf8"))

        adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
        cmd = adb + " shell am force-stop " + package_name
        console_result = subprocess.check_output(cmd, shell=True)
        time.sleep(1)
        print(console_result.decode("utf8"))

        adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
        cmd = adb + " shell am start -n " + package_name + '/' + activity_name.replace(package_name, '')
        console_result = subprocess.check_output(cmd, shell=True)
        time.sleep(1)
        print(console_result.decode("utf8"))


# 这个代码后期要改变，因为不一定是activity
def lead_to_function(package_name, activity_name, search_action_list):
    '''
    print("回到功能入口")
    # 启动功能活动，其中活动名要去掉其中的包名，命令为 “adb shell am start -n {包名 / 活动名}”
    # adb需要自己添加路径？？这里要该到自己的adb去
    adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
    cmd = adb + " shell am start -n " + package_name + '/' + activity_name.replace(package_name, '')
    console_result = subprocess.check_output(cmd, shell=True)
    print(console_result.decode("utf8"))
    '''
    device = u2.connect()
    device.press("back")
    time.sleep(0.5)
    launch_act(package_name, activity_name)
    for search_result_action in search_action_list:
        exec(search_result_action)
        time.sleep(1)

def perform_the_action(action_list):
    # 执行action跳转到制定entry
    device = u2.connect()
    print("执行的跳转活动：", action_list)
    if len(action_list) != 0:
        for action in action_list:
            print(action)
            exec(action)
            time.sleep(0.7)


def to_entry(action_list, package_name, activity_name):
    '''
    # 先跳转到特定的activity
    if 'MainActivity' not in activity_name:
        adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
        cmd = adb + " shell am start -n " + package_name + '/' + activity_name.replace(package_name, '')
        console_result = subprocess.check_output(cmd, shell=True)
        print(console_result.decode("utf8"))
        # 执行action跳转到指定entry
        perform_the_action(action_list)
    else:
        print(package_name, activity_name)
        # 不知道为什么，MainActivity不能冷启动
        adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
        cmd = adb + " shell am start -n " + package_name + '/' + activity_name.replace(package_name, '')
        console_result = subprocess.check_output(cmd, shell=True)
        time.sleep(2)
        print(console_result.decode("utf8"))

        adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
        cmd = adb + " shell am force-stop " + package_name
        console_result = subprocess.check_output(cmd, shell=True)
        time.sleep(2)
        print(console_result.decode("utf8"))

        adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
        cmd = adb + " shell am start -n " + package_name + '/' + activity_name.replace(package_name, '')
        console_result = subprocess.check_output(cmd, shell=True)
        time.sleep(2)
        print(console_result.decode("utf8"))
    '''
    launch_act(package_name, activity_name)
    perform_the_action(action_list)


if __name__ == '__main__':
    # lead_to_function("gov.anzong.androidnga", "gov.anzong.androidnga.activity.SettingsActivity")
    # launch_app("gov.anzong.androidnga", "gov.anzong.androidnga.activity.SettingsActivity")
    # to_entry(["device(text='USER AGENT').click()", "device(text='CANCEL').click()"], "gov.anzong.androidnga", "gov.anzong.androidnga.activity.SettingsActivity")
    to_entry([""], "gov.anzong.androidnga", "gov.anzong.androidnga.activity.MainActivity")