import hashlib
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element

def get_vector(dxml, project):
    vector_str = ""
    child_stack = []
    ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')
    with open(dxml, 'rt') as f:
        tree = ET.parse(f)
    '''
    tree = ET.XML(dxml)   
    
    '''
    root = ""
    for node in tree.iter():
        if node.tag == "hierarchy":
            root = node
            break
    # print(root.attrib)
    for child in root:
        # print(child.tag, child.attrib)
        if child.attrib['package'] == project:
            child_stack.append(child)

    while len(child_stack) > 0:
        m = hashlib.md5()
        root = child_stack.pop()
        info = root.attrib
        if info['class'] != "android.widget.FrameLayout":
            tmpstr = info['resource-id'] + info['class'] + info['package']
            m.update(tmpstr.encode("utf8"))
            vector_str = vector_str + m.hexdigest()
        elif info['class'] == "android.widget.FrameLayout":
            if len(root) != 0:
            #if not root[0] == None and not root[0]:
                tmpstr = info['resource-id'] + info['class'] + info['package']
                m.update(tmpstr.encode("utf8"))
                vector_str = vector_str + m.hexdigest()
        if root.attrib['class'] == "android.widget.ListView":
            if root.getchildren() != []:
                child_stack.append(root[0])
        else:
            for child in root:
                child_stack.append(child)
    vector = hashlib.md5()
    vector.update(vector_str.encode("utf8"))
    return vector.hexdigest()

if __name__ == '__main__':
    get_vector("xml文件名", "包名")