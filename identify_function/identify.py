import os
import random
import time

import uiautomator2 as u2

import xml_analyse


def launch_apk(apk):
    # 连接设备
    device = u2.connect()

    # 打印设备信息
    print(device.device_info)

    # 获取apk的package名称
    apk_without_version = apk.split('_')[0]

    # 查看apk是否已经安装
    if not device.app_info(apk_without_version):
        # 安装apk
        input_apk = '../in_put/' + apk
        device.app_install(input_apk)

    # 打开app
    device.app_start(apk_without_version)


def identify_function():
    # 连接设备
    device = u2.connect()
    time.sleep(1)

    # dump layout文件
    # 字典，包含目前apk的包名和活动名
    apk_cur_info = device.app_current()
    print(apk_cur_info)

    # 若不存在当前apk的文件夹，则创建文件夹
    result_url = '../result/'
    layout_url = '../result/' + apk_cur_info['package'] + '/layout/'
    screenshot_url = '../result/' + apk_cur_info['package'] + '/screenshot/'

    if not os.path.exists(result_url):
        os.makedirs(result_url)
    if not os.path.exists(layout_url):
        os.makedirs(layout_url)
    if not os.path.exists(screenshot_url):
        os.makedirs(screenshot_url)

    # 若为同一个act的不同scene，则为xml文件的活动名改名
    if os.path.exists(layout_url + apk_cur_info['activity'] + '.xml'):
        apk_cur_info['activity'] = apk_cur_info['activity'] + random.randint(1,20000).__str__()

    # dump xml文件
    with open(layout_url + apk_cur_info['activity'] + '.xml', 'w', encoding='UTF-8') as f:
        f.write(device.dump_hierarchy())

    # 截屏
    device.screenshot(screenshot_url + apk_cur_info['activity'] + '.png')

    # 分析xml文件
    xml_analyse.xmlAnalyseStart(apk_cur_info['package'])


if __name__ == '__main__':
    identify_function()
