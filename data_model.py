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

class CommentDetail(Base):
    __tablename__='t_comment_detail'

    sid=Column(Integer,primary_key=True)
    guid=Column(VARCHAR(36))
    product_id=Column(Integer)
    comment_source=Column(Integer)
    dp_site=Column(VARCHAR(100))
    walk_aim=Column(VARCHAR(100))
    content=Column(TEXT)
    image_urls=Column(TEXT)
    image_count=Column(Integer)
    rating=Column(VARCHAR(10))
    dp_date=Column(DATETIME)
    is_elite=Column(BOOLEAN)
    item_name=Column(TEXT)
    prize_jiangjin=Column(FLOAT)
    user_level=Column(Integer)
    user_name=Column(VARCHAR(100))
    vote_count=Column(Integer)

class CommentDetailMerged(Base):
    __tablename__='t_comment_detail_merged'

    sid=Column(Integer,primary_key=True)
    guid=Column(VARCHAR(36))
    product_id_group=Column(TEXT)
    comment_source=Column(Integer)
    dp_site=Column(VARCHAR(100))
    walk_aim=Column(VARCHAR(100))
    content=Column(TEXT)
    image_urls=Column(TEXT)
    image_count=Column(Integer)
    rating=Column(VARCHAR(10))
    dp_date=Column(DATETIME)
    is_elite=Column(BOOLEAN)
    item_name=Column(TEXT)
    prize_jiangjin=Column(FLOAT)
    user_level=Column(Integer)
    user_name=Column(VARCHAR(100))
    vote_count=Column(Integer)

class CommentImage(Base):
    __tablename__='t_comment_image'

    sid=Column(Integer,primary_key=True)
    guid=Column(VARCHAR(36))
    pic_url=Column(TEXT)