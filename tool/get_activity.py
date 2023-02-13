import re
import os

import uiautomator2 as u2


# 获取当前activity，得到的activity信息之只有最后一部分
def get_current_activity():
    '''
    adb = "/home/xiaobudian/Android/Sdk/platform-tools/adb"
    # 读取当前页面
    content = os.popen(adb + ' shell dumpsys activity  |grep "mResumedActivity" ').read()
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
    return apk_cur_info['activity'].split('.')[-1]


if __name__ == '__main__':
    print(get_current_activity())
