import logging
from sqlalchemy import Column, NVARCHAR, Integer, TEXT, DATETIME, BOOLEAN, VARCHAR, FLOAT
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

Base = declarative_base()


class ProductMain(Base):
    __tablename__ = 't_product_main'

    sid = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    source = Column(VARCHAR(100))
    destination = Column(VARCHAR(100))
    product_name = Column(TEXT)
    product_name_append = Column(TEXT)
    product_highlight = Column(TEXT)
    purchased_count = Column(Integer)
    comment_count = Column(Integer)
    least_price = Column(FLOAT)

class CommentMain(Base):
    __tablename__='t_comment_main'

    sid=Column(Integer,primary_key=True)
    product_id=Column(Integer)
    comment_count=Column(Integer)
    good_count=Column(Integer)
    mid_count=Column(Integer)
    bad_count=Column(Integer)
    with_photo_count=Column(Integer)