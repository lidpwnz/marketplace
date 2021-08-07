from http_fw.base_controller import BaseController
from http_fw.template_engine import get_template
from databases.repositories.cars_repository import CarsRepository


class CarsController(BaseController):
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
              <div class="car-price">{car.price}</div>
          </div>
      </div>           
            """

        tmp = get_template('static/list.html', {'cars': body})

        self.response.add_header('Content-Type', 'text/html')
        self.response.set_body(tmp)
