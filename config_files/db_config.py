from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///shop.db', echo=True)

Session = sessionmaker(bind=engine)
current_session = scoped_session(Session)

Base = declarative_base()


def create_tables():
    Base.metadata.create_all(engine)


def remove_session():
    current_session.remove()


def get_session():
    if current_session.is_active:
        return current_session

    return Session()
