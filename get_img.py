import requests
from pyquery import PyQuery
import json


def get_stu_list(path):
    with open(path, 'r', encoding='utf-8') as f:
        stu_list = json.load(f)
    return stu_list


def save_stu(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)
        print("保存数据成功")


def get_image_url(name, id):
    if not name or not id:
        return ""
    url = 'http://www.cltt.org/StudentScore/ScoreResult'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36'
    }
    data = {
        'name': name,
        'idCard': id
    }
    try:
        res = requests.post(url, data=data, headers=headers).text
    except requests.ConnectionError:
        print(name + '查询异常')
        return ""

    doc = PyQuery(res)
    img_src = doc('.user-img').find('img').attr('src')
    if not img_src:
        return ""
    else:
        return img_src


def handle_img(stu_list):
    """
    得到学生照片地址，并作为键值对存入学生列表中
    :param stu_list: 学生信息列表
    :return: 更新后的学生信息列表
    """
    img_src_list = []
    for i, stu in enumerate(stu_list):
        if i % 100 == 0:
            print('已经处理100组数据')
        id_card = stu['id_card'].strip()
        name = stu['name']
        img_src = get_image_url(name, id_card)
        stu['img'] = img_src
        img_src_list.append(img_src)
    return stu_list


def main():
    stu_list = get_stu_list('stu_info.json')
    handle_img(stu_list)  # 拿到学生照片，并存入stu中
    save_stu(stu_list, 'stu_info_img.json')  # 重新保存学生信息


if __name__ == '__main__':
    main()
