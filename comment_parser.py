from bs4 import BeautifulSoup
import os
import json
import data_model
import db_tool
import env


def parse_comment_detail():
    db_session=db_tool.Session(env.connect_str)
    for json_file in os.listdir('comment_json_pages'):
        abs_filename = 'comment_json_pages/'+json_file
        reader = open(abs_filename, 'r', encoding='utf-8')
        json_line = reader.readline().strip('\n')
        try:
            comment_dict:dict = json.loads(json_line)
        except json.decoder.JSONDecodeError:
            print(json_file)
            continue
        if 'iserror' in comment_dict.keys():
            continue
        comments=comment_dict['dpList']
        models=[]
        for comment in comments:
            model=data_model.CommentDetail()
            model.comment_source=comment['commentSource']
            model.content=comment['DPContent']
            model.dp_date=comment['DPDate']
            model.dp_site=comment['DPSite']
            model.guid=comment['DPGuid']
            model.image_count=comment['imageCount']
            model.is_elite=comment['DPIsElite']
            model.item_name=comment['DPItemName']
            model.prize_jiangjin=comment['DPPrize_JiangJin']
            model.product_id=int(json_file.split('_')[0])
            model.rating=comment['DPRating']
            model.user_level=comment['DPUserLevel']
            model.user_name=comment['DPUserName']
            images=comment['DPImagesStr'].split(',')
            image_models=[]
            for image in images:
                    if image=='':
                        continue
                    image_model=data_model.CommentImage()
                    image_model.guid=comment['DPGuid']
                    image_model.pic_url=image
                    image_models.append(image_model)
            db_session.db_list_writer(image_models)        
            models.append(model)
        db_session.db_list_writer(models)
        print('Finish {0}'.format(json_file))
    db_session.close_session()

def parse_comment_main():
    db_session = db_tool.Session(env.connect_str)
    file_names = os.listdir('comment_json_pages')
    file_names = list(filter(lambda o: o.split('_')
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

parse_comment_detail()