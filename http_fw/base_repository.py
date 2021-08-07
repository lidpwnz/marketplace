

class BaseRepository:
    _model = None

    def __init__(self, session):
        self.db = session

    def delete(self, id: int):
        self._model.query.filter_by(id=id).delete()

    def find(self, **kwargs):
        return self.db.query(self._model).get(kwargs.get('id'))

    def all(self):
        return self.db.query(self._model).all()

    def add(self, **kwargs) -> None:
        post = self._model(**kwargs)

        self.db.add(post)
        self.db.commit()

