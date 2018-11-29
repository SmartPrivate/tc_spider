import requests
import json
import random
import time
import os
import db_tools.db_tool as db_tool
import db_tools.data_model as data_model


def load_header_dict():
    reader = open('config/header.txt', 'r', encoding='utf-8')
    lines = reader.readlines()
    header = {}
    for line in lines:
        if line[0] == '#':
            continue
        line = line.strip('\n')
        key, value = line.split(': ')
        header[key] = value
    return header


def get_comments_by_product_id(product_id, comment_count, header_dict):
    pages = int(comment_count/100)
    if comment_count % 100:
        pages = pages+1
    for i in range(1, pages+1):
        params_dict = dict(productId=product_id, page=i, pageSize=100)
        base_url = 'https://gny.ly.com/fetch/comment'
        r = requests.get(url=base_url, headers=header_dict, params=params_dict)
        if r.status_code == 200:
            file_name = str(product_id)+'_'+str(i)+'.json'
            writer_comment_file(file_name, r.text)
            print('完成{0}第{1}页'.format(str(product_id), str(i)))
            time.sleep(random.randint(0, 5))
        else:
            print(r.status_code)
            exit(1)


def writer_comment_file(file_name, comment_text):
    file_dir = os.path.join('comment_json_pages', file_name)
    if os.path.exists(file_dir):
        os.remove(file_dir)
    writer = open(file_dir, 'a', encoding='utf-8')
    writer.write(comment_text)
    writer.close()


connect_str=open('config/connect_str.txt','r',encoding='utf-8').readline().strip('\n')
db_session = db_tool.Session(connect_str)
models = db_session.query_product_with_comment()
for model in models:
    model: data_model.ProductMain
    if model.sid < 564:
        continue
    get_comments_by_product_id(
        model.product_id, model.comment_count, load_header_dict())
# to-do
# sid 528