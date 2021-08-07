from http_fw.server import run
from config_files.urls import router
from config_files import db_config as db

config_dict = {
    'host': 'localhost',
    'port': 8000,
    'static_img': 'static/img',
    'static_css': 'static/css'
}

db.create_tables()

run(router, config_dict)
