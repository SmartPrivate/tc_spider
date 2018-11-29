import requests
import os
from bs4 import BeautifulSoup
import json
import time
import random


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


def save_html_file(html_text, filename):
    file_dir = os.path.join('html_pages', filename)
    if os.path.exists(file_dir):
        os.remove(file_dir)
    writer = open(file_dir, 'a', encoding='utf-8')
    writer.write(html_text)
    writer.close()


def get_list_page(source: str, destination: str, page_index: int, file_name: str):
    base_url = 'https://gny.ly.com/list'
    params_dict = dict(src=source, dest=destination)
    params_dict['start'] = str(page_index)
    header_dict = load_header_dict()
    r = requests.get(url=base_url, params=params_dict, headers=header_dict)
    if r.status_code == 200:
        save_html_file(r.text, file_name)
        print('页面文件已写入{0}'.format(file_name))
    else:
        print(r.status_code)


def get_list_pages(source: str, destination: str, page_index: int, end_page_index: int):
    for i in range(page_index, end_page_index + 1):
        page_file = '{0}_{1}_page_{2}.html'.format(source, destination, str(i))
        get_list_page(source=source, destination=destination,
                      page_index=i, file_name=page_file)
        time.sleep(random.randint(1, 5))


get_list_pages(source='武汉', destination='厦门', page_index=50, end_page_index=58)
