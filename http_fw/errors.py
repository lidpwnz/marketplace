from .request import Request
from .response import Response


def not_found(request: Request, response: Response):
    response.set_status(Response.HTTP_NOT_FOUND)
    response.add_header('Content-Type', 'text/html')

    response.set_body('<h1>Not Found</h1>')


def internal_server_error(request: Request, response: Response):
    response.set_status(Response.HTTP_INTERNAL_SERVER_ERROR)
    response.add_header('Content-Type', 'text/html')

    response.set_body('<h1>Internal Server Error</h1>')
