# -*- coding: utf-8 -*-
"""
 * Description:
 * @author: xiaobudian
 * @date: 2022.12.23
"""

import xml.etree.ElementTree as et
import os
import numpy as np

from tool import eigenvector


# 判断是否为控件容器
def isContainer(node):
    # 容器控件类型集合，可以扩充
    containerSet = {'android.widget.ListView', 'android.view.ViewGroup', 'android.widget.HorizontalScrollView', 'androidx.recyclerview.widget.RecyclerView', 'android.widget.TableRow', 'android.support.v7.widget.RecyclerView'}
    if 'class' in node.attrib and node.attrib['class'] in containerSet:
        return True
    return False


# 判断一定不是功能入口的控件（造成干扰的class）
def isDistractorClass(node):
    # 不作为功能入口的控件类型，可以扩充
    # Spinner暂时有争议，等到探讨完可行性再说
    distractorSet = {'android.widget.EditText', 'android.widget.Spinner'}
    if 'class' in node.attrib and node.attrib['class'] in distractorSet:
        return True
    return False


def have_this_function(node_dict):
    list_url = '../result/' + appName + '/' + appName + '.npy'
    temp_list = np.load(list_url, allow_pickle=True).tolist()
    for temp_dict in temp_list:
        if temp_dict['function_name'] == node_dict['function_name']:
            return True
    return False


def update_function(node_dict):
    list_url = '../result/' + appName + '/' + appName + '.npy'
    temp_list = np.load(list_url, allow_pickle=True).tolist()
    temp_list.append(node_dict)
    np.save(list_url, np.array(temp_list))


# 遍历子节点取功能语义
def getSemantics(node):
    childrenNode = list(node)
    # 若节点不是叶子节点
    if len(childrenNode) != 0:
        # 先判断一下，如果子节点中有checkable的节点则淘汰
        for child in childrenNode:
            if child.attrib['checkable'] == 'true':
                return ''
        # 取语义
        for child in childrenNode:
            # # 若checkable则不取语义
            # if child.attrib['checkable'] == 'true':
            #     return ''
            # 取子节点语义作为自身语义
            if getSemantics(child) != '':
                return getSemantics(child)
            # 若子节点没有语义，则取自身节点信息作为语义
            else:
                if child.attrib['text'] != '':
                    return child.attrib['text']
                elif child.attrib['content-desc'] != '':
                    return child.attrib['content-desc']
        return ''
    # 若节点为叶子节点
    if node.attrib['text'] != '':
        return node.attrib['text']
    elif node.attrib['content-desc'] != '':
        return node.attrib['content-desc']
    # elif node.attrib['resource-id'] != '':
    #     return node.attrib['resource-id']
    return ''


# 提取功能
def extraction(node):
    # 提取的功能
    func = list()
    # 从第一层子节点提取功能
    childrenNode = list(node)
    if len(childrenNode) == 0:
        return func
    for child in childrenNode:
        # 若可以点击，不为editText、spinner，则提取其功能语义
        if child.attrib['clickable'] == 'true' and child.attrib['checkable'] == 'false' and not isDistractorClass(child):
            semantics = getSemantics(child)
            if semantics != '':
                temp_dict = func_dict
                temp_dict['function_name'] = semantics
                temp_dict['widget'] = et.tostring(child, encoding='unicode').split('\n')[0]
                if not have_this_function(temp_dict):
                    update_function(temp_dict)
                func.append(semantics)
    return func


# 遍历xml文件
def traversal(rootNode, level):
    # print(level, rootNode.tag, rootNode.attrib,'\n')
    # 判断相关的控件是否为容器控件，并提取功能语义
    if isContainer(rootNode):
        # 提取语义功能
        # print(level, rootNode.tag, rootNode.attrib)
        # print(extraction(rootNode), '\n')
        if len(extraction(rootNode)) != 0:
            # recordModule(rootNode.tag.__str__() + rootNode.attrib.__str__() + '\n')
            print(level, rootNode.tag, rootNode.attrib)
            recordModule(extraction(rootNode).__str__() + '\n')
            print(extraction(rootNode), '\n')

    # 递归子节点实现遍历
    childrenNode = list(rootNode)
    # 递归出口
    if len(childrenNode) == 0:
        return
    # 递归
    for child in childrenNode:
        traversal(child, level + 1)
    return


# xml文件分析代码入口函数
def xmlTest(fileName):
    # 取每个apk的layout文件夹中的xml文件
    xmlList = os.listdir(fileName)
    for xmlfile in xmlList:
        if '.xml' in xmlfile:
            func_dict['activity'] = xmlfile.split('.xml')[0].split('Activity')[0] + 'Activity'
            func_dict['ui_hash'] = eigenvector.get_vector(appLayoutURL + xmlfile, appName)
            # 取xml文件
            print(xmlfile)
            recordModule('\n' + xmlfile + '\n')
            tree = et.ElementTree(file=fileName + '/' + xmlfile)
            root = tree.getroot()
            # 遍历xml节点，参数为根节点、层数
            traversal(root, 1)


def recordModule(message):
    filename = '../result/' + appName + '/' + appName + '.txt'
    with open(filename, 'a', encoding='UTF-8') as f:
        f.write(message)


def xmlAnalyseStart(package_name):
    global appLayoutURL
    global appName
    global func_dict
    func_dict = {'function_name': '', 'widget': '', 'package': package_name, 'activity': '', 'ui_hash': ""}
    appName = package_name
    appLayoutURL = '../result/' + appName + '/layout/'

    # 格式化txt文件
    filename = '../result/' + appName + '/' + appName + '.txt'
    with open(filename, 'w', encoding='UTF-8') as f:
        f.write('')

    list_url = '../result/' + appName + '/' + appName + '.npy'
    if os.path.exists(list_url):
        os.remove(list_url)
    tempList = []
    np.save(list_url, np.array(tempList))

    # 执行分析
    xmlTest(appLayoutURL)
    # .npy -> .txt
    list_url = '../result/' + appName + '/' + appName + '.npy'
    temp_list = np.load(list_url, allow_pickle=True).tolist()

    temp_fileurl = '../result/' + appName + '/' + appName + '_function.txt'
    with open(temp_fileurl, 'w', encoding='UTF-8') as f:
        f.write('')

    for temp_dict in temp_list:
        with open(temp_fileurl, 'a', encoding='UTF-8') as f:
            f.write(str(temp_dict) + '\n')
        print(temp_dict)


if __name__ == '__main__':
    xmlAnalyseStart('gov.anzong.androidnga')
