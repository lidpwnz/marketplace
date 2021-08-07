from glob import glob
import os


class StaticResponder:
    def __init__(self, request, response, static_dir) -> None:
        self.request = request
        self.response = response
        self.static_dir = static_dir
        self.file = None
        self._check_file()

    def _check_file_url(self):
        """Задаем корректный путь до папки с картинками"""
        file_url = self.request.url.replace('..', '')
        if file_url.endswith('.css'):
            return file_url, 'css'

        static_file = file_url.split('/')[-1]
        return f'/{static_file}', 'img'

    def _check_file(self) -> None:
        """Проверяем запрос на валидность"""
        file_url, file_type = self._check_file_url()

        if file_type == 'css':
            self.static_dir = 'static/css'

        path = './' + self.static_dir + file_url
        files = glob(path)

        if len(files) > 0 and os.path.isfile(files[0]):
            self.file = files[0]

    def prepare_response(self) -> None:
        file = open(self.file, 'rb')
        self.response.set_file_body(file)
