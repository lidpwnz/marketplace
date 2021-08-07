from databases.repositories.makes_repository import MakeRepository
from http_fw.base_controller import BaseController
from http_fw.errors import not_found
from http_fw.response import Response
from http_fw.template_engine import get_template
from databases.repositories.cars_repository import CarsRepository
from http_fw.helpers import get_item_by_id
from models.car_model import Car


class CarsController(BaseController):
    def __parse_body(self) -> dict:
        result = {key: int(value) if value.isdigit() else value for key, value in self.request.body.items()}

        if 'image' not in result:
            result['image'] = 'https://vintage-crimea.ru/wp-content/uploads/2018/01/net-foto.png'

        return result

    def _get_make_options(self, car: Car = None) -> str:
        makes_list = MakeRepository(self.context).all()
        options = ''

        for make in makes_list:
            if car and int(car.make_id) == make.id:
                options += f'<option value="{make.id}" selected>{make.title}</option>'

            else:
                options += f'<option value="{make.id}">{make.title}</option>'

        return options

    def _get_cars_list_html(self) -> str:
        cars_repository = CarsRepository(self.context)
        cars = cars_repository.all()

        body = ''
        for car in cars:
            body += f"""
         <div class="d-flex mb-4">
            <span class="car-img-box">
                <img src="{car.image}" class="car-image" alt="{car.make}">
            </span>
            <div class="d-flex flex-column">
                <a class="car-make" href="/advertisements/detail?id={car.id}">{car.make} ({car.year})</a>
                <div class="car-price">${car.price}</div>
            </div>
        </div>           
              """

        return body

    def list(self) -> None:
        tmp = get_template('static/advertisements/list.html', {'cars': self._get_cars_list_html()})

        self.response.add_header('Content-Type', 'text/html')
        self.response.set_body(tmp)

    def new(self) -> None:
        tmp = get_template('static/advertisements/advertisement.html', {'make_options': self._get_make_options(),
                                                                        'url': '/advertisements/add',
                                                                        'btn': 'Create',
                                                                        'page_title': 'Place new advertisement'})

        self.response.add_header('Content-Type', 'text/html')
        self.response.set_body(tmp)

    def create(self) -> None:
        cars_repository = CarsRepository(self.context)
        cars_repository.add(**self.__parse_body())

        self.response.set_status(Response.HTTP_MOVED_PERMANENTLY)
        self.response.add_header('Location', '/')

    def detail(self) -> None:
        car = get_item_by_id(id=self.request.query_params.get('id'), repository=CarsRepository(self.context))
        if car:
            tmp = get_template('static/advertisements/detail.html', {**vars(car),
                                                                     'make': car.make})

            self.response.add_header('Content-Type', 'text/html')
            self.response.set_body(tmp)
        else:
            not_found(self.request, self.response)

    def delete(self) -> None:
        cars_repository = CarsRepository(self.context)
        cars_repository.delete(id=self.request.query_params.get('id'))

        self.response.set_status(Response.HTTP_MOVED_PERMANENTLY)
        self.response.add_header('Location', '/')

    def update_get(self) -> None:
        car = get_item_by_id(id=self.request.query_params.get('id'), repository=CarsRepository(self.context))
        tmp = get_template('static/advertisements/advertisement.html', {**vars(car),
                                                                        'make_options': self._get_make_options(car),
                                                                        'url': '/advertisements/update',
                                                                        'btn': 'Edit',
                                                                        'page_title': 'Update advertisement'})

        self.response.add_header('Content-Type', 'text/html')
        self.response.set_body(tmp)

    def update_post(self) -> None:
        cars_repository = CarsRepository(self.context)
        data = self.request.body
        cars_repository.update(id=data.get('id'), values=data)

        self.response.set_status(Response.HTTP_MOVED_PERMANENTLY)
        self.response.add_header('Location', '/')
