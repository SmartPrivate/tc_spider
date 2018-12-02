from bs4 import BeautifulSoup
import os
import json
import data_model
import db_tool
import env


def parse_comment_detail():
    db_session = db_tool.Session(env.connect_str)
    for json_file in os.listdir('comment_json_pages'):
        abs_filename = 'comment_json_pages/'+json_file
        reader = open(abs_filename, 'r', encoding='utf-8')
        json_line = reader.readline().strip('\n')
        try:
            comment_dict: dict = json.loads(json_line)
        except json.decoder.JSONDecodeError:
            print(json_file)
            continue
        if 'iserror' in comment_dict.keys():
            continue
        comments = comment_dict['dpList']
        models = []
        for comment in comments:
            model = data_model.CommentDetail()
            model.comment_source = comment['commentSource']
            model.dp_site = comment['DPSite']
            model.walk_aim=comment['walkAim']
            model.content = comment['DPContent']
            model.rating = comment['DPRating']
            model.image_count = comment['imageCount']
            model.dp_date = comment['DPDate']
            model.guid = comment['DPGuid']
            model.is_elite = comment['DPIsElite']
            model.item_name = comment['DPItemName']
            model.prize_jiangjin = comment['DPPrize_JiangJin']
            model.product_id = int(json_file.split('_')[0])
            model.user_level = comment['DPUserLevel']
            model.user_name = comment['DPUserName']
            model.vote_count=comment['DPVoteCount']
            model.image_urls = comment['DPImagesStr']
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


def get_comment_guid_distinct():
    db_session = db_tool.Session(env.connect_str)
    models = db_session.query_all(data_model.CommentDetail)
    guid_set = set(list(map(lambda o: o.guid, models)))
    total_count = len(guid_set)
    count = 0
    for guid in guid_set:
        distinct_models = list(filter(lambda o: o.guid == guid, models))
        product_id_list = list(
            map(lambda o: str(o.product_id), distinct_models))
        merged_model = data_model.CommentDetailMerged()
        merged_model.product_id_group = ','.join(product_id_list)
        distinct_model = distinct_models[0]
        props = dir(distinct_model)
        for prop in props:
            if prop[0] == '_':
                continue
            setattr(merged_model, prop, getattr(distinct_model, prop))
        db_session.db_writer(merged_model)
        count = count+1
        print('Finished {0}/{1}'.format(str(count), str(total_count)))

def image_parser():
    db_session=db_tool.Session(env.connect_str)
    models=db_session.query_all(data_model.CommentDetailMerged)
    with_image_models=list(filter(lambda o:o.image_count>0,models))
    
    for model in with_image_models:
        image_models=[]
        model: data_model.CommentDetailMerged
        for url in model.image_urls.split(','):
            image_model=data_model.CommentImage()
            image_model.guid=model.guid
            image_model.pic_url=url
            image_models.append(image_model)
        db_session.db_list_writer(image_models)
