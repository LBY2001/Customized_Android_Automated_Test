import re
import os
import subprocess

import uiautomator2 as u2


# 获取当前包名
def get_current_package():
    # 连接设备
    device = u2.connect()
    # 字典，包含目前apk的包名和活动名
    apk_cur_info = device.app_current()
    print(apk_cur_info)
    return apk_cur_info['package']

# 获取当前activity，得到的activity信息之只有最后一部分
def get_current_activity():
    '''
    # 读取当前页面
    content = os.popen('adb shell dumpsys activity  |grep "mResumedActivity" ').read()
    # 正则表达式提取activity
    pattern = re.compile(r'/[a-zA-Z0-9\.]+')
    alist = pattern.findall(content)
    print(alist)
    # 取activity名称
    current_activity = ""
    # 这里都设置-1对吗？
    if len(alist) != 0:
        current_activity = alist[-1].split('.')[-1]
    else:
        print(content)
    return current_activity
    '''
    # 连接设备
    device = u2.connect()
    # 字典，包含目前apk的包名和活动名
    apk_cur_info = device.app_current()
    print(apk_cur_info)
    # return apk_cur_info['activity'].split('.')[-1]
    return apk_cur_info['activity']


# 通过apk获取启动活动，eg: com.utazukin.ichaival.ArchiveList
def get_launch_activity(apk_path):
    # 获取启动活动
    result = subprocess.check_output(
        r"aapt dump badging " + apk_path + " | grep launchable-activity | awk '{print $2}'",
        shell=True)
    # 处理命令行结果
    launch_activity = result.decode('utf-8').split('name=\'')[1].split('\'')[0]
    return launch_activity


# 通过apk获取版本号
def get_version(apk_path):
    result = subprocess.check_output(
        "aapt dump badging " + apk_path + " | grep versionName | awk '{print $3}' | sed s/versionCode=//g | sed s/\\\'//g",
        shell=True)
    return result.decode('utf-8').split('\n')[0]


def get_package_name(apk_path):
    pkg_line = subprocess.check_output(
        "aapt dump badging " + apk_path + " | grep package",
        shell=True)
    defined_pkg_name = pkg_line.decode('utf-8').split('\'')[1]
    pkg_name = ""
    launcher = get_launch_activity(apk_path)
    if launcher == '' or defined_pkg_name in launcher or launcher.startswith("."):
        pkg_name = defined_pkg_name
    else:
        pkg_name = launcher.replace('.' + launcher.split('.')[-1], '').split('\'')[1]
    return pkg_name


# 通过apk获取标准apk名称
def get_new_app_name(apk_path):
    return get_package_name(apk_path) + '_' + get_version(apk_path) + '.apk'
    

if __name__ == '__main__':
    print(get_current_package())
    # print(get_launch_activity("../input_apk_test/2_com.csnmedia.android.bg_4f478_2015-12-04.apk"))
    # print(get_version("../input_apk_test/2_com.csnmedia.android.bg_4f478_2015-12-04.apk"))
    # print(get_new_app_name("../input_apk_test/2_com.csnmedia.android.bg_4f478_2015-12-04.apk"))
