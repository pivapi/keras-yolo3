import xml.etree.ElementTree as ET
from os import getcwd
'''
这个文件的目的是将xml格式的annotation文件转换为txt的annotation文件
'''

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert_annotation(year, image_id, list_file):
    '''
    具体实现细节需要结合调试源代码才能弄懂了
    '''
    in_file = open('/home/piva/Datasets/PASCAL-VOC/VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

# wd = getcwd()
wd = '/home/piva/Datasets/PASCAL-VOC'

for year, image_set in sets:
    # 得到一个数据集里面所有图片的ID
    image_ids = open('/home/piva/Datasets/PASCAL-VOC/VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    # 依次新建并打开train val test三个annotation文件 
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        # 首先将图片的路径写入行首
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg'%(wd, year, image_id))
        # 再将图片里面GT信息写入每一行
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
    list_file.close()

