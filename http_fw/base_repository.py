from sqlalchemy import delete, update, select
from models.car_model import Car


class BaseRepository:
    _model = None

    def __init__(self, session):
        self.db = session

    def delete(self, id: str):
        stmt = delete(self._model).where(self._model.id == int(id))

        self.db.execute(stmt)
        self.db.commit()

    def find(self, **kwargs):
        return self.db.query(self._model).get(kwargs.get('id'))

    def find_by_parameter(self, first_param, second_param, session):
        stmt = select(self._model).where(getattr(self._model, first_param) == second_param)

        result = session.execute(stmt)
        cars = []
        for i in result.scalars():
            cars.append(i)

        return cars

    def all(self):
        return self.db.query(self._model).all()

    def add(self, **kwargs) -> None:
        post = self._model(**kwargs)

        self.db.add(post)
        self.db.commit()

    def update(self, id: str, values: dict):
        stmt = update(self._model).where(self._model.id == int(id)).values(**values)

        self.db.execute(stmt)
        self.db.commit()
