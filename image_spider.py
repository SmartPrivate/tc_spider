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
    guid_tuple_list = list(map(lambda o: (o.guid,o.pic_url), models))
    guid_list=set(list(map(lambda o:o[0],guid_tuple_list)))
    total_count=len(guid_list)
    for item in guid_list:
        count=0
        pics=list(filter(lambda o:o[0]==item,guid_tuple_list))
        pic_count=len(pics)
        for i in range(pic_count):
            file_name='{0}.jpg'.format(str(i))
            abs_file_name=os.path.join('images',item,file_name)
            image_stream=requests.get(url=pics[i][1]).content
            with open(abs_file_name,'wb') as w:
                w.write(image_stream)
            time.sleep(0.1)
        count=count+1
        print('已完成{0}/{1}'.format(count,total_count))


download_pic()