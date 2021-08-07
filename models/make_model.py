from config_files.db_config import Base
from sqlalchemy import Integer, String, Column


class Make(Base):
    __tablename__ = 'makes'

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)

    def __repr__(self):
        return self.title
