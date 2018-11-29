from bs4 import BeautifulSoup
import os
import json
import db_tools.data_model as data_model
import db_tools.db_tool as db_tool
import config.env as env


def parse_comment_detail():
    for json_file in os.listdir('comment_json_pages'):
        abs_filename = 'comment_json_pages/'+json_file
        reader = open(abs_filename, 'r', encoding='utf-8')
        json_line = reader.readline().strip('\n')
        comment_dict = json.loads(json_line)
        print(comment_dict.keys())
        print(comment_dict['count'])
        break


def parse_comment_main():
    db_session = db_tool.Session(env.connect_str)
    file_names = os.listdir('comment_json_pages')
    file_names = list(filter(lambda o: o.spilt('_')
                             [1] == '1.json', file_names))
    for file_name in file_names:
        abs_filename = os.path.join('comment_json_pages', file_name)
        comment_dict: dict = json.loads(
            open(abs_filename, 'r', encoding='utf-8').readline().strip('\n'))
        if 'iserror' in comment_dict.keys():
            continue
        model = data_model.CommentMain()
        model.product_id = int(file_name.split('_')[0])
        model.comment_count = comment_dict['count']['allNumber']
        model.good_count = comment_dict['count']['goodNumber']
        model.mid_count = comment_dict['count']['modeNumber']
        model.bad_count = comment_dict['count']['negativeNumber']
        model.with_photo_count = comment_dict['count']['photoNumber']
        db_session.db_writer(model)
    db_session.close_session()


def get_comment_product_id_set():
    dirs = []
    for json_file in os.listdir('comment_json_pages'):
        dir_name: str = json_file.split('_')[0]
        dirs.append(dir_name)
    dirs = set(dirs)
    return dirs


def move_file_to_dir():
    dirs = os.listdir('comment_json_pages/')
    os.path.isdir()


parse_comment_main()
