from controllers.cars_controller import CarsController
from controllers.makes_controller import MakesController
from http_fw.router import Router

router = Router()
router.get('/', CarsController, 'list')
router.get('/advertisements', CarsController, 'list')
router.get('/advertisements/add', CarsController, 'new')
router.post('/advertisements/add', CarsController, 'create')
router.get('/advertisements/detail', CarsController, 'detail')
router.post('/advertisements/delete', CarsController, 'delete')
router.get('/advertisements/update', CarsController, 'update_get')
router.post('/advertisements/update', CarsController, 'update_post')

router.get('/makes', MakesController, 'list')
router.get('/makes/add', MakesController, 'new')
router.post('/makes/add', MakesController, 'create')
router.get('/makes/detail', MakesController, 'detail')
router.get('/makes/update', MakesController, 'update_get')
router.post('/makes/update', MakesController, 'update_post')
router.post('/makes/delete', MakesController, 'delete')


