from urllib.parse import parse_qs


class Request:
    """
    Распарсили запрос на микрочасти
    """

    def __init__(self, file) -> None:
        self.file = file
        self.method, self.url, self.protocol, self.body = [None for _ in range(4)]
        self.headers = {}
        self.query_params = {}

        self.parse_request_line()
        self.parse_headers()
        self.parse_body()
        self._parse_specific_body()

    def parse_request_line(self) -> None:
        request_line = self.read_line()
        self.method, self.url, self.protocol = request_line.split()
        self.parse_request_url()

        if self.protocol != 'HTTP/1.1':
            raise ValueError('Wrong protocol!')

    def parse_request_url(self):
        req = self.url.split('?')

        if len(req) > 1:
            self.url = req.pop(0)
            query_string = req[0].split('&')

            for param in query_string:
                key, value = param.split('=')
                self.query_params[key] = value

    def read_line(self) -> str:
        return self.file.readline().decode().strip()

    def parse_headers(self) -> None:
        while True:
            header = self.read_line()

            if not header:
                break

            header_name, header_value = header.split(': ')
            self.headers[header_name] = header_value

    def parse_body(self) -> None:
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            self.body = self.file.read(content_length)

    def _parse_specific_body(self) -> None:
        if 'Content-Type' in self.headers and self.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            parsed_string = parse_qs(bytes(self.body).decode())
            self.body = {key: value[0] for key, value in parsed_string.items()}
