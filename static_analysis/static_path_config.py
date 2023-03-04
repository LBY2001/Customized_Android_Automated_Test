# 静态分析包共享配置，用户自行更改配置
class Path:
    java_home_path = '/usr/lib/jvm/jdk1.8.0_45'
    sdk_platform_path = 'config/libs/android-platforms/'
    lib_home_path = 'config/libs/'
    callbacks_path = 'config/AndroidCallbacks.txt'
    jadx_path = 'config/jadx-master/'

    config_path = 'config/'
    soot_jar = 'config/getSootOutput-Ubuntu.jar'
    soot_binary = 'config/run_soot.run'

    ic3_path = 'config/IC3/'
    ic3_home = ic3_path + 'ic3-0.2.0/'
    ic3_jar = ic3_home + 'ic3-0.2.0-full.jar'
    ic3_android_jar = ic3_home + 'android.jar'
