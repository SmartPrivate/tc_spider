import requests
import db_tool
import data_model
import env
import os
import time


def make_pic_dir():
    db_session = db_tool.Session(env.connect_str)
    models = db_session.query_all(data_model.CommentImage)
    guid_list = list(map(lambda o: o.guid, models))
    print(len(guid_list))
    guid_list = set(guid_list)
    print(len(guid_list))
    for item in guid_list:
        os.makedirs('images/{0}'.format(item))


def download_pic():
    db_session = db_tool.Session(env.connect_str)
    models = db_session.query_all(data_model.CommentImage)
    guid_tuple_list = list(map(lambda o: (o.guid, o.pic_url), models))
    guid_list = set(list(map(lambda o: o[0], guid_tuple_list)))
    guid_list = list(guid_list)
    total_count = len(guid_list)
    for index in range(total_count):
        if index < 4375:
            continue
        pics = list(filter(lambda o: o[0] ==
                           guid_list[index], guid_tuple_list))
        pic_count = len(pics)
        for i in range(pic_count):
            file_name = '{0}.jpg'.format(str(i))
            abs_file_name = os.path.join('images', guid_list[index], file_name)
            image_url = pics[i][1]
            try:
                image_stream = requests.get(url=image_url).content
            except:
                print('图片{0}无法下载！'.format(image_url))
                with open('error_image_url.txt', 'a', encoding='utf-8') as err_f:
                    err_f.write(image_url+'\n')
                continue
            if os.path.exists(abs_file_name):
                continue
            with open(abs_file_name, 'wb') as w:
                w.write(image_stream)
        print('已完成{0}/{1}'.format(index, total_count))


def error_image_parser():
    reader = open('error_image_url.txt', 'r', encoding='utf-8')
    lines = reader.readlines()
    urls = []
    for line in lines:
        if line == '\n':
            continue
        urls.append(line.strip('\n'))
    db_session = db_tool.Session(env.connect_str)
    models = db_session.query_image_models_by_urls(urls)
    for model in models:
        print(model.guid)
        print(model.pic_url)

error_image_parser()