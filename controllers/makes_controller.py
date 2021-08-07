from databases.repositories.makes_repository import MakeRepository
from http_fw.base_controller import BaseController
from http_fw.errors import not_found
from http_fw.response import Response
from http_fw.template_engine import get_template
from http_fw.helpers import get_item_by_id


class MakesController(BaseController):
    def __parse_body(self):
        return {key: int(value) if value.isdigit() else value for key, value in self.request.body.items()}

    def _get_makes_list_html(self):
        makes_repository = MakeRepository(self.context)
        makes = makes_repository.all()

        body = ''
        for make in makes:
            body += f"""
        <div class="d-flex mb-4">
            <div class="d-flex flex-column">
                <a class="car-make" href="/makes/detail?id={make.id}">{make.title}</a>
            </div>
        </div>           
              """

        return body

    def list(self):
        tmp = get_template('static/makes/list.html', {'makes': self._get_makes_list_html(),
                                                      'page_title': 'Makes'})

        self.response.add_header('Content-Type', 'text/html')
        self.response.set_body(tmp)

    def new(self):
        tmp = get_template('static/makes/make.html', {'url': '/makes/add',
                                                      'btn': 'Create',
                                                      'page_title': 'Create new make'})

        self.response.add_header('Content-Type', 'text/html')
        self.response.set_body(tmp)

    def create(self):
        makes_repository = MakeRepository(self.context)
        makes_repository.add(**self.__parse_body())

        self.response.set_status(Response.HTTP_MOVED_PERMANENTLY)
        self.response.add_header('Location', '/makes')

    def detail(self):
        make = get_item_by_id(id=self.request.query_params.get('id'), repository=MakeRepository(self.context))
        if make:
            tmp = get_template('static/makes/detail.html', {**vars(make)})

            self.response.add_header('Content-Type', 'text/html')
            self.response.set_body(tmp)
        else:
            not_found(self.request, self.response)

    def delete(self):
        makes_repository = MakeRepository(self.context)
        makes_repository.delete(id=self.request.query_params.get('id'))

        self.response.set_status(Response.HTTP_MOVED_PERMANENTLY)
        self.response.add_header('Location', '/makes')

    def update_get(self):
        make = get_item_by_id(id=self.request.query_params.get('id'), repository=MakeRepository(self.context))
        tmp = get_template('static/makes/make.html', {**vars(make),
                                                      'url': '/makes/update',
                                                      'btn': 'Edit',
                                                      'page_title': 'Update Maker'})

        self.response.add_header('Content-Type', 'text/html')
        self.response.set_body(tmp)

    def update_post(self):
        makes_repository = MakeRepository(self.context)
        data = self.request.body
        makes_repository.update(id=data.get('id'), values=data)

        self.response.set_status(Response.HTTP_MOVED_PERMANENTLY)
        self.response.add_header('Location', '/makes')
