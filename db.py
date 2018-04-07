from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

db_url = 'mysql+pymysql://mga2j:justice23@mgajustice-db.cu92s72c9cow.us-east-1.rds.amazonaws.com/mga_justice?charset=utf8&use_unicode=0'

Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(db_url, convert_unicode=True, pool_size=100, pool_recycle=3600))
session = scoped_session(Session)