from controllers.cars_controller import CarsController
from http_fw.router import Router

router = Router()
router.get('/', CarsController, 'list')
router.get('/advertisements', CarsController, 'list')
router.get('/advertisements/add', CarsController, 'new')
router.post('/advertisements/add', CarsController, 'create')
router.get('/advertisements/detail', CarsController, 'detail')

