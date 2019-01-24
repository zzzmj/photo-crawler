import json
import os
import time
from urllib.request import urlretrieve


def get_stu_list(path):
    with open(path, 'r', encoding='utf-8') as f:
        stu_list = json.load(f)
    for stu in stu_list:
        if not stu['img']:
            continue
        college = stu['college']
        stu_class = stu['class']
        directory = college + '/' + stu_class
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = '{}/{}/{}.jpeg'.format(college, stu_class, stu['name'])
        urlretrieve(stu['img'], filename=filename)
    return stu_list


def main():
    get_stu_list('stu_info_img.json')


if __name__ == '__main__':
    st = time.time()
    main()
    ed = time.time()
    print("爬取学生图片一共花费时间：", ed-st)
