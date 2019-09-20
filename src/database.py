from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:root@postgres-wiki-parser:5432/postgres', pool_size=20)
Session = sessionmaker(bind=engine)

Base = declarative_base()
