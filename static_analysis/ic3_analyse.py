import os
import time

from .static_path_config import Path
from tool import get_activity


def ic3(apk_path, package_name):
    # 存IC3结果
    results_IC3 = IC3_output_dir + package_name + '.txt'
    with open(results_IC3, 'w') as f:
        f.write('')
    # 执行IC3分析
    if (os.system('timeout 15m java -Xmx4g -jar %s -apkormanifest %s -in %s -cp %s -protobuf %s | grep "PATH: "'
                  % (IC3_jar, apk_path, soot_output_dir, IC3_android_jar, IC3_output_dir))) != 0:
        ic3_info = 'Failure'
        with open(IC3_fail_file, 'w') as f:
            f.write(apk_path + '\n')
    else:
        ic3_info = 'Success'

    print('Running IC3: ' + ic3_info)
    return results_IC3, ic3_info


def parse_IC3(file, pkg):
    dict = {}
    if not os.path.exists(file):
        return
    f = open(file, 'r')
    line = f.readline()
    flag = -1
    s = 0 # indicate component
    brace = 0 # indicate the number of braces
    while line:
        if '{' in line:
            brace += 1
        if '}' in line:
            brace -= 1
        if 'components {' in line:
            s = 1
            flag = -1
            tmp =''
            brace = 1
        elif s == 1 and 'name:' in line:
            tmp = line.split(': "')[1].split('"')[0]
            s = 2
        elif s == 2 and 'kind: ACTIVITY' in line:
            flag = 0
            sourceActivity = tmp
            s = 3
        elif flag == 0 and "exit_points" in line:
            flag = 1
        elif flag == 1 and 'statement' in line:
            stm = line.split(': "')[1].split('"')[0]
            flag = 2
        elif flag == 2 and 'method: "' in line:
            mtd = line.split(': "<')[1].split('>"')[0]
            flag = 3
        elif flag == 3 and 'kind: ' in line:
            if 'kind: ACTIVITY' in line:
                flag = 4
            else:
                flag = 0
        elif flag == 4 and 'kind: CLASS' in line:
            flag = 5
        elif flag == 5 and 'value' in line:
            if ': "L' in line:
                targetActivity = line.strip().split(': "L')[1].split(';"')[0].replace('/', '.')
                if targetActivity.endswith('"'):
                    targetActivity = targetActivity.split('"')[0]
            else:
                targetActivity = line.strip().split(': "')[1].split(';"')[0].replace('/', '.')
                if targetActivity.endswith('"'):
                    targetActivity = targetActivity.split('"')[0]
            if not pkg in targetActivity:
                flag = 0
                continue
            if not sourceActivity in dict.keys():
                dict[sourceActivity] = set()
            dict[sourceActivity].add(targetActivity)
            flag = 4
        if brace == 1 and s == 3: # in component, find more exit_points
            flag = 0
        line = f.readline()

    # 保存信息
    IC3_output_dir = "../result/" + pkg + "/IC3/IC3_output/"
    results_parseIC3_dir = IC3_output_dir + 'parsed_ic3/'
    if not os.path.exists(results_parseIC3_dir):
        os.makedirs(results_parseIC3_dir)
    IC3_atg = results_parseIC3_dir + pkg + '.txt'
    with open(IC3_atg, 'w') as f:
        f.write('')
    for k, v in dict.items():
        for v1 in v:
            with open(IC3_atg, 'a') as f:
                f.write(k + '-->' + v1 + '\n')

    return dict


def get_ic3_output(apk_path):
    # 初始化配置
    global IC3_path, IC3_jar, soot_output_dir, IC3_fail_file, IC3_output_dir, IC3_home, IC3_android_jar, package_name
    IC3_jar = Path.ic3_jar
    IC3_home = Path.ic3_home
    IC3_path = Path.ic3_path
    IC3_android_jar = Path.ic3_android_jar

    # 收集ic3_Output
    package_name = get_activity.get_package_name(apk_path)
    soot_output_dir = "../result/" + package_name + "/soot_output/"
    IC3_fail_file = "../result/" + package_name + "/IC3/IC3_fail.txt"
    IC3_output_dir = "../result/" + package_name + "/IC3/IC3_output/"
    if not os.path.exists(IC3_output_dir):
        os.makedirs(IC3_output_dir)
    start_time = time.time()
    ic3_output, ic3_info = ic3(apk_path, package_name)
    end_time = time.time()
    run_time = end_time - start_time  # 程序的运行时间，单位为秒
    print('ic3与运行时间：', run_time)

    # 解析ic3结果生成at，可能结果为空
    version = get_activity.get_version(apk_path)
    dict = parse_IC3(ic3_output.split('.txt')[0] + '_' + version + '.txt', package_name)
    print(dict)
    return dict


if __name__ == '__main__':
    # get_ic3_output("../input_apk_test/gov.anzong.androidnga_3080.apk")
    dict = parse_IC3("../result/gov.anzong.androidnga/IC3/IC3_output/gov.anzong.androidnga_3080.txt", 'gov.anzong.androidnga')
    print(dict)
