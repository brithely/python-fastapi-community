import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


def get_mysql_uri():
    host = os.environ.get("DB_HOST")
    port = 3306
    password = os.environ.get("DB_PASSWORD")
    user = os.environ.get("DB_USER")
    db_name = os.environ.get("DB_DATABASE")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(get_mysql_uri())
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_session():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
