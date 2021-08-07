class BaseModel:
    _id_generator = None

    def __init__(self):
        self.id = next(self._id_generator)
