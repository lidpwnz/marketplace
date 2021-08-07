from databases.repositories.makes_repository import MakeRepository
from http_fw.base_controller import BaseController
from http_fw.response import Response
from http_fw.template_engine import get_template
from databases.repositories.cars_repository import CarsRepository


class CarsController(BaseController):

    def _parse_body(self):
        result = {key: int(value) if value.isdigit() else value for key, value in self.request.body.items()}

        if 'image' not in result:
            result['image'] = 'https://vintage-crimea.ru/wp-content/uploads/2018/01/net-foto.png'

        return result

    def _get_make_options(self):
        makes_list = MakeRepository(self.context).all()
        options = ''

        for make in makes_list:
            options += f'<option value="{make.id}">{make.title}</option>'

        return options

    def list(self):
        cars_repository = CarsRepository(self.context)
        cars = cars_repository.all()

        body = ''
        for car in cars:
            body += f"""
       <div class="d-flex">
          <span class="car-img-box">
              <img src="{car.image}" class="car-image" alt="{car.make}">
          </span>
          <div class="d-flex flex-column">
              <a class="car-make" href="/advertisements/detail?id={car.id}">{car.make} ({car.year})</a>
              <div class="car-price">${car.price}</div>
          </div>
      </div>           
            """

        tmp = get_template('static/list.html', {'cars': body})

        self.response.add_header('Content-Type', 'text/html')
        self.response.set_body(tmp)

    def new(self):
        tmp = get_template('static/new.html', {'make_options': self._get_make_options()})

        self.response.add_header('Content-Type', 'text/html')
        self.response.set_body(tmp)

    def create(self):
        cars_repository = CarsRepository(self.context)
        cars_repository.add(**self._parse_body())

        self.response.set_status(Response.HTTP_MOVED_PERMANENTLY)
        self.response.add_header('Location', '/')

