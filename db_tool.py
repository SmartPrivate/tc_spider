from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import data_model

class Session(object):
    def __init__(self, connect_str):
        engine = create_engine(connect_str)
        self.__session = sessionmaker(
            bind=engine, autoflush=False, expire_on_commit=False)()

    def db_writer(self, model):
        self.__session.add(model)
        self.__session.commit()

    def db_list_writer(self, models):
        self.__session.bulk_save_objects(models)
        self.__session.commit()
    
    def close_session(self):
        self.__session.close()

    def query_all(self,model_name):
        return self.__session.query(model_name).all()

    def query_product_with_comment(self):
        return self.__session.query(data_model.ProductMain).filter(data_model.ProductMain.comment_count>0).all()