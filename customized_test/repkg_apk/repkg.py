import os
import shutil
import subprocess

import tool.get_activity


def repackage(apk_url):
    # 定义需要处理的APK文件路径和单个任务（singleTask）字符串以及单个顶部（singleTop）字符串
    single_task = 'singleTask'
    single_top = 'singleTop'
    password = '123456'
    signed_name = tool.get_activity.get_package_name(apk_url) + "_signed.apk"

    try:
        # 执行apktool反编译apk
        os.system(f'apktool d {apk_url} -o temp')

        # 获取AndroidManifest.xml文件的路径
        manifest_file = os.path.join('temp', 'AndroidManifest.xml')

        # 判断AndroidManifest.xml文件是否存在单个任务
        with open(manifest_file, 'r') as f:
            if single_task in f.read():
                # 如果存在单个任务，替换所有的单个任务为单个顶部
                with open(manifest_file, 'r') as f2:
                    content = f2.read().replace(single_task, single_top)
                with open(manifest_file, 'w') as f3:
                    f3.write(content)
                # 重新编译APK
                os.system('apktool b temp')
                # 获取重新编译后的APK文件的路径
                apk_name = os.listdir(os.path.join('temp', 'dist'))[0]
                apk_file = os.path.join('temp', 'dist', apk_name)
                # 对APK进行签名
                cmd = ['jarsigner', '-verbose', '-keystore', 'apk_key.jks', '-signedjar', signed_name, apk_file, 'key0']
                result = subprocess.run(cmd, input=password.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # 输出命令的输出和错误信息
                print(result.stdout.decode())
                print(result.stderr.decode())
                # 删除temp目录
                shutil.rmtree('temp')
                # 将新生成的签名APK移动到原来APK所在的目录中
                target_dir = os.path.dirname(os.path.abspath(apk_url))
                target_file = os.path.join(target_dir, os.path.basename(signed_name))
                if os.path.exists(target_file):
                    os.remove(target_file)
                shutil.move(signed_name, target_file)
                print("重新打包成功")
                return True, target_file
            else:
                print(f"{manifest_file}文件中没有需要更改的字符，不进行重新打包和签名。")
                # 删除temp目录
                shutil.rmtree('temp')
                return False, apk_url
    except Exception as e:
        print("重新打包失败")
        return False, apk_url

if __name__ == '__main__':
    repackage("/home/xiaobudian/PycharmProjects/GraduationProject/crash_apk2/YourLocalWeather-debug.apk")
    # signed_name = "org.thosp.yourlocalweather_signed.apk"
    # apk_url = "/home/xiaobudian/PycharmProjects/GraduationProject/crash_apk2/YourLocalWeather-debug.apk"
    # shutil.move(signed_name, os.path.dirname(os.path.abspath(apk_url)))
