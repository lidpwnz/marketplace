from typing import Any


def parse_request_query_params(request_url: str) -> (str, dict):
    query_params: dict = {}
    parsed_url: list = request_url.split('?')
    url = parsed_url.pop(0)

    if parsed_url:
        params = parsed_url[0].split('&')

        for param in params:
            key, value = param.split('=')
            query_params[key] = value

    return url, query_params


def get_id() -> iter:
    i = 0
    while True:
        i += 1
        yield i


def hasattr_valid(db, var):
    if not hasattr(db, var):
        raise TypeError(f'Undefined column! {var}')


def foreign_key(database: Any, id: int):
    db = database()
    return db.find({'id': id})


def get_item_by_id(id, repository):
    return repository.find(id=id)
