from models.car_model import Car
from http_fw.base_repository import BaseRepository


class CarsRepository(BaseRepository):
    _model = Car

