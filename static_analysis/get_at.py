import os

from tool import get_activity


def get_at(apk_path):
    package_name = get_activity.get_package_name(apk_path)
    version = get_activity.get_version(apk_path)
    soot_at_file = "../result/" + package_name + "/soot_test_output/storydroid_atgs/" + package_name + '_' + version + '.txt'
    ic3_at_file = "../result/" + package_name + "/IC3/IC3_output/parsed_ic3/" + package_name + '.txt'
    # 打开ic3与soot的at文件
    with open(soot_at_file, 'r') as f:
        lines_sootatg = f.readlines()
    with open(ic3_at_file, 'r') as f:
        lines_ic3atg = f.readlines()
    # 整合为一个at
    total_atg = set()
    for line in lines_sootatg:
        total_atg.add(line)
    for line in lines_ic3atg:
        total_atg.add(line)
    # save
    atg_dir = "../result/" + package_name + "/static_atg/"
    if not os.path.exists(atg_dir):
        os.makedirs(atg_dir)
    atg_file = atg_dir + 'static_atg.txt'
    with open(atg_file, 'a') as f:
        for item in total_atg:
            f.write(item)
    


if __name__ == '__main__':
    get_at("../input_apk_test/gov.anzong.androidnga_3080.apk")
