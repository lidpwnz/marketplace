from http_fw.response import Response
from http_fw.request import Request
from config_files.db_config import get_session


class BaseController:
    def __init__(self, request: Request, response: Response):
        self.request: Request = request
        self.response: Response = response
        self.context = get_session()
