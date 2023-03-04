import os

from tool import get_activity
from static_path_config import Path


def soot(apk_path, package_name):
    print('java -jar ', soot_jar, soot_output_dir, package_name, test_output_dir, apk_path)
    # os.chdir(test_output_dir + '/config/')
    os.system('java -jar %s %s %s %s %s' % (soot_jar, soot_output_dir, package_name, test_output_dir, apk_path))


def get_soot_atg(apk_path):
    package_name = get_activity.get_package_name(apk_path)
    soot_binary = Path.soot_binary
    java_home_path = Path.java_home_path
    sdk_platform_path = Path.sdk_platform_path
    lib_home_path = Path.lib_home_path
    test_output_dir = "../result/" + package_name + "/soot_test_output/"

    results_enhancedIC3_label = test_output_dir + 'outputs/' + package_name + '/activity_paras.txt'
    if os.path.exists(results_enhancedIC3_label):
        return

    # Using binary
    os.system('%s %s %s %s %s %s %s' % (
    soot_binary, test_output_dir, apk_path, package_name, java_home_path, sdk_platform_path, lib_home_path))
    '''
    Using jar

    enhancedIC3_jar = output + 'config/run_soot.jar'
    os.chdir(output)
    os.system('java -jar %s %s %s %s %s %s %s' % (enhancedIC3_jar, output, apk_path, pkg_name, java_home_path, sdk_platform_path, lib_home_path))
    '''

def get_soot_output(apk_path):
    # 初始化配置
    global soot_jar, soot_output_dir, test_output_dir
    soot_jar = Path.soot_jar

    # 收集sootOutput
    package_name = get_activity.get_package_name(apk_path)
    soot_output_dir = "../result/" + package_name + "/soot_output/"
    test_output_dir = "../result/" + package_name + "/soot_test_output/"
    if not os.path.exists(soot_output_dir):
        os.makedirs(soot_output_dir)
    if not os.path.exists(test_output_dir):
        os.makedirs(test_output_dir)
    soot(apk_path, package_name)


if __name__ == '__main__':
    # get_soot_output("../input_apk_test/gov.anzong.androidnga_3080.apk")
    get_soot_atg("../input_apk_test/a2dp.Vol_169.apk")
