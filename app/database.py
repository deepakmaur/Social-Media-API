from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting
# SQLALCHEMY_DATABSE_URL='postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

# engine=createEngine(SQLALCHEMY_DATABSE_URL)

SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

# a dependecy required for orm
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()



