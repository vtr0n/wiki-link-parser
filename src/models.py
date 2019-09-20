from sqlalchemy import Column, Integer, String, ForeignKey
from src.database import Base, engine


class Pages(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    URL = Column(String)
    request_depth = Column(Integer)


class Dependencies(Base):
    __tablename__ = 'dependencies'

    id = Column(Integer, primary_key=True)
    from_page_id = Column(Integer, ForeignKey('pages.id'))
    link_id = Column(Integer, ForeignKey('pages.id'))


Base.metadata.create_all(engine)
