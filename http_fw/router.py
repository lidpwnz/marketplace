from typing import Any
from .errors import not_found, internal_server_error
from .request import Request
from .response import Response


class Router:
    def __init__(self) -> None:
        self.routes: dict = {
            'get': [],
            'post': []
        }

    def _add(self, http_method: str, url: str, ctrl: Any, method: Any) -> None:
        self.routes[http_method].append(
            {
                'url': url,
                'ctrl': ctrl,
                'method': method
            }
        )

    def get(self, *args) -> None:
        self._add('get', *args)

    def post(self, *args) -> None:
        self._add('post', *args)

    def run(self, request: Request, response: Response) -> Any:
        method_routes = self.routes[request.method.lower()]
        route = None

        for r in method_routes:
            if r['url'] == request.url:
                route = r
                break

        else:
            return not_found(request, response)

        # noinspection PyBroadException
        # try:
        ctrl = route['ctrl'](request, response)
        getattr(ctrl, route.get('method'))()
        #
        # except BaseException:
        #     return internal_server_error(request, response)
