from sqlalchemy.orm import relationship

from config_files.db_config import Base
from sqlalchemy import Integer, String, Column, ForeignKey

from models.make_model import Make


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    make_id = Column(String(150), ForeignKey('makes.id'), nullable=False)
    make = relationship(Make, foreign_keys='Car.make_id')
    year = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String(200), nullable=True)
    description = Column(String(1000), nullable=True)
    contacts = Column(String(300), nullable=False)

    def __repr__(self):
        return f'{self.id} {self.make}'
