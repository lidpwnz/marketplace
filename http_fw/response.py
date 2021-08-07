from os import fstat


class Response:
    """Собираем ответ"""

    HTTP_OK: int = 200
    HTTP_BAD_REQUEST: int = 400
    HTTP_NOT_FOUND: int = 404
    HTTP_INTERNAL_SERVER_ERROR: int = 500
    HTTP_MOVED_PERMANENTLY: int = 301

    MESSAGES: dict = {
        HTTP_OK: 'OK',
        HTTP_BAD_REQUEST: 'Bad Request',
        HTTP_NOT_FOUND: 'Not Found',
        HTTP_INTERNAL_SERVER_ERROR: 'Internal Server Error',
        HTTP_MOVED_PERMANENTLY: 'Moved Permanently'
    }

    PROTOCOL: str = 'HTTP/1.1'

    def __init__(self, file) -> None:
        self.file = file
        self.status: int = self.HTTP_OK
        self.headers = []
        self.body = None
        self.file_body = None

    def set_file_body(self, file) -> None:
        self.file_body = file
        size = fstat(file.fileno()).st_size
        self.add_header('Content-Length', str(size))

    def set_body(self, body: str) -> None:
        self.body = body.encode()
        self.add_header('Content-Length', str(len(self.body)))

    def add_header(self, name: str, value: str) -> None:
        self.headers.append({'name': name, 'value': value})

    def set_status(self, status: int) -> None:
        self.status = status

    def _get_status_line(self) -> str:
        if self.status in self.MESSAGES:
            message: str = self.MESSAGES.get(self.status)
        else:
            message = ''

        return f'{self.PROTOCOL} {self.status} {message}'

    def _get_response_head(self) -> bytes:
        status_line = self._get_status_line()

        headers = [status_line]

        for header in self.headers:
            headers.append(f'{header["name"]}: {header["value"]}')

        head_str = '\r\n'.join(headers)
        head_str += '\r\n\r\n'

        return head_str.encode()

    def _write_file_body(self) -> None:
        while True:
            data = self.file_body.read(1024)
            if not data:
                break

            self.file.write(data)

    def send(self) -> None:
        head = self._get_response_head()
        self.file.write(head)

        if self.body:
            self.file.write(self.body)
        if self.file_body:
            self._write_file_body()
