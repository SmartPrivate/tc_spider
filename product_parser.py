from bs4 import BeautifulSoup
import db_tools.db_tool as db_tool
import db_tools.data_model as data_model
import os

def parse_list_page_to_data_model(file_name):
    soup = BeautifulSoup(open(file_name, encoding='utf-8'), 'lxml')
    items = soup.find_all('a', 'route-link')
    model_list=[]
    for item in items:
        model=data_model.ProductMain()
        product_id=item.get('href')[11:-9]
        model.product_id=int(product_id)
        whole_name:str=item.find('em').get('title')
        model.product_name=whole_name.split('<')[0]
        model.product_name_append=whole_name.split('<')[1].strip('>')
        model.product_highlight=item.find('p','ell').find('em').text
        model.source=file_name.split('/')[-1].split('_')[0]
        model.destination=file_name.split('/')[-1].split('_')[1]
        try:
            model.purchased_count=int(item.find('p','person-num').text.split('人')[0])
        except AttributeError:
            model.purchased_count=0
        try:
            model.comment_count=int(item.find('p','person-comment').text.split('条')[0])
        except AttributeError:
            model.comment_count=0
        try: 
            model.least_price=float(item.find('strong').text)
        except AttributeError:
            model.least_price=0.0     
        model_list.append(model)
    return model_list
    
def parse_list_page(src,des,page_index):
    connect_str=open('config/connect_str.txt','r',encoding='utf-8').readline().strip('\n')
    db_session=db_tool.Session(connect_str)
    for i in range(1,page_index+1):
        filename=r'html_pages/{1}_{2}_page_{0}.html'.format(str(i),src,des)
        models=parse_list_page_to_data_model(file_name=filename)
        db_session.db_list_writer(models)
    db_session.close_session()

parse_list_page('武汉','厦门',58)
