from sqlalchemy import delete


class BaseRepository:
    _model = None

    def __init__(self, session):
        self.db = session

    def delete(self, id: int):
        stmt = delete(self._model).where(self._model.id == int(id))

        self.db.execute(stmt)
        self.db.commit()

    def find(self, **kwargs):
        return self.db.query(self._model).get(kwargs.get('id'))

    def all(self):
        return self.db.query(self._model).all()

    def add(self, **kwargs) -> None:
        post = self._model(**kwargs)

        self.db.add(post)
        self.db.commit()

